# main.py

from library import Library


def main():
    """
    Main function to run the command-line interface for the library application.
    """
    lib = Library()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book (by ISBN)")
        print("2. Remove Book")
        print("3. List Books")
        print("4. Find Book")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            isbn = input("Enter the 10 or 13-digit ISBN of the book: ").strip()
            if isbn:
                lib.add_book(isbn)
            else:
                print("Error: ISBN cannot be empty.")

        elif choice == '2':
            isbn = input("Enter ISBN of the book to remove: ")
            lib.remove_book(isbn)

        elif choice == '3':
            lib.list_books()

        elif choice == '4':
            isbn = input("Enter ISBN of the book to find: ")
            book = lib.find_book(isbn)
            if book:
                print(f"Found book: {book}")
            else:
                print(f"No book found with ISBN {isbn}.")

        elif choice == '5':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
