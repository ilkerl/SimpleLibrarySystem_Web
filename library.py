# library.py

import json
import httpx
from book import Book


class Library:
    """
    Manages the collection of books, including fetching data from the Open Library API.
    """

    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = self.load_books()
        self.api_url = "https://openlibrary.org/api/books"

    def load_books(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Book(item['title'], item['author'], item['isbn']) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self):
        with open(self.filename, 'w') as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)

    def add_book(self, isbn):
        """
        Fetches book data from the Open Library API using its ISBN and adds it.
        """
        if self.find_book(isbn):
            print(f"Error: Book with ISBN {isbn} already exists.")
            return None

        print(f"Fetching book data for ISBN: {isbn}...")
        params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}

        try:
            response = httpx.get(self.api_url, params=params, timeout=10.0)
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
            self.books.append(new_book)
            self.save_books()
            print(f"Successfully added: {new_book}")
            return new_book

        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
            return None

    def remove_book(self, isbn):
        book_to_remove = self.find_book(isbn)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"Book removed: {book_to_remove}")
            return True
        else:
            return False

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def list_books(self):

        return self.books
