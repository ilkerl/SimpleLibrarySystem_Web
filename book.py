# book.py

class Book:
    """
    Represents a single book in the library.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The International Standard Book Number, used as a unique identifier.
    """

    def __init__(self, title, author, isbn):
        """
        Initializes a new Book object.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            isbn (str): The ISBN of the book.
        """
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        """
        Returns a user-friendly string representation of the book.
        This is called when you use print() on a Book object.

        Example: "Ulysses by James Joyce (ISBN: 978-0199535675)"

        Returns:
            str: The formatted string representation of the book.
        """
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn})'

    def to_dict(self):
        """
        Converts the Book object to a dictionary.
        This is useful for JSON serialization.

        Returns:
            dict: A dictionary representation of the book.
        """
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn
        }
