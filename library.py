# library.py

import os
import psycopg2
import psycopg2.extras
import httpx
from book import Book

class Library:
    """
    Manages the collection of books using a robust connection strategy for PostgreSQL.
    """

    def __init__(self, db_url):
        """
        Initializes the library with the database URL and ensures the table exists.
        """
        if not db_url:
            raise ValueError("Database connection URL is required.")
        self.db_url = db_url
        self._initialize_database()

    def _get_connection(self):
        """Helper method to create and return a new database connection."""
        return psycopg2.connect(self.db_url)

    def _initialize_database(self):
        """
        Connects to the database once at startup to create the 'books' table
        if it doesn't already exist.
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS books (
                        isbn TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL
                    )
                """)
            conn.commit()
        except psycopg2.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            if conn:
                conn.close()

    def add_book(self, isbn):
        """
        Fetches book data and adds it to the database using a fresh connection.
        """
        if self.find_book(isbn):
            print(f"Error: Book with ISBN {isbn} already exists.")
            return None

        # Fetching from Open Library API remains the same
        api_url = "https://openlibrary.org/api/books"
        params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}
        try:
            response = httpx.get(api_url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            if not data or f"ISBN:{isbn}" not in data:
                return None
            book_data = data[f"ISBN:{isbn}"]
            title = book_data.get("title", "Unknown Title")
            authors = book_data.get("authors", [])
            author_names = ", ".join([a['name'] for a in authors]) if authors else "Unknown Author"
            new_book = Book(title, author_names, isbn)
        except httpx.RequestError as e:
            print(f"API request error: {e}")
            return None

        # Database operation with a new connection
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO books (isbn, title, author) VALUES (%s, %s, %s)",
                    (new_book.isbn, new_book.title, new_book.author)
                )
            conn.commit()
            print(f"Successfully added: {new_book}")
            return new_book
        except psycopg2.Error as e:
            print(f"Database Error on add: {e}")
            if conn: conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    def remove_book(self, isbn):
        """Removes a book from the database using a fresh connection."""
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM books WHERE isbn = %s", (isbn,))
                was_removed = cursor.rowcount > 0
            conn.commit()
            return was_removed
        except psycopg2.Error as e:
            print(f"Database Error on remove: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def find_book(self, isbn):
        """Finds a book in the database using a fresh connection."""
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
                row = cursor.fetchone()
                if row:
                    return Book(title=row['title'], author=row['author'], isbn=row['isbn'])
            return None
        except psycopg2.Error as e:
            print(f"Database Error on find: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def list_books(self):
        """Returns a list of all books using a fresh connection."""
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM books")
                return [dict(row) for row in cursor.fetchall()]
        except psycopg2.Error as e:
            print(f"Database Error on list: {e}")
            return [] # Return an empty list on error
        finally:
            if conn:
                conn.close()
