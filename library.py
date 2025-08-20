# library.py

import os
import psycopg2
import psycopg2.extras # Sözlük olarak sonuç almak için
import httpx
from book import Book

class Library:
    """
    Manages the collection of books using a PostgreSQL database.
    """

    def __init__(self, db_url):
        """
        Initializes the library and connects to the PostgreSQL database.
        Creates the 'books' table if it doesn't exist.
        """
        if not db_url:
            raise ValueError("Database connection URL is required.")
        self.conn = psycopg2.connect(db_url)
        self.create_table()

    def create_table(self):
        """Creates the 'books' table in the database if it's not already there."""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    isbn TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL
                )
            """)
        self.conn.commit()

    def add_book(self, isbn):
        """
        Fetches book data from the Open Library API and adds it to the database.
        """
        if self.find_book(isbn):
            print(f"Error: Book with ISBN {isbn} already exists.")
            return None

        print(f"Fetching book data for ISBN: {isbn}...")
        api_url = "https://openlibrary.org/api/books"
        params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}

        try:
            response = httpx.get(api_url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            if not data or f"ISBN:{isbn}" not in data:
                print(f"Error: No book found with ISBN {isbn}.")
                return None

            book_data = data[f"ISBN:{isbn}"]
            title = book_data.get("title", "Unknown Title")
            authors = book_data.get("authors", [])
            author_names = ", ".join([author['name'] for author in authors]) if authors else "Unknown Author"

            new_book = Book(title, author_names, isbn)

            with self.conn.cursor() as cursor:
                # PostgreSQL'de placeholder olarak '?' yerine '%s' kullanılır
                cursor.execute(
                    "INSERT INTO books (isbn, title, author) VALUES (%s, %s, %s)",
                    (new_book.isbn, new_book.title, new_book.author)
                )
            self.conn.commit()
            print(f"Successfully added: {new_book}")
            return new_book

        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
            return None
        except psycopg2.Error as e:
            print(f"Database Error: {e}")
            self.conn.rollback() # Hata durumunda işlemi geri al
            return None

    def remove_book(self, isbn):
        """Removes a book from the database using its ISBN."""
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE isbn = %s", (isbn,))
            # cursor.rowcount silinen satır sayısını verir
            was_removed = cursor.rowcount > 0
        self.conn.commit()
        return was_removed

    def find_book(self, isbn):
        """Finds a book in the database by its ISBN."""
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
            row = cursor.fetchone()
            if row:
                # DictCursor sayesinde sütun adlarıyla erişebiliriz
                return Book(title=row['title'], author=row['author'], isbn=row['isbn'])
        return None

    def list_books(self):
        """Returns a list of all books from the database as dictionaries."""
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM books")
            # Sonucu doğrudan bir sözlük listesine çevir
            return [dict(row) for row in cursor.fetchall()]

    def __del__(self):
        """Destructor to close the database connection."""
        if self.conn:
            self.conn.close()
