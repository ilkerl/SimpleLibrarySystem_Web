# Simple Library System

This is a three-stage library management system developed as part of the Python 202 Bootcamp hosted by Global AI Hub.. The project starts as a simple command-line application, is enhanced with data from an external API, and finally evolves into a service that provides its own web API.

## Stages

**1. OOP Terminal Application:** Creating the basic library functionalities using Object-Oriented Programming principles.

**2. External API Integration:** Automatically fetching book information using an ISBN via the Open Library API.

**3. Web Service with FastAPI:** Transforming the library logic into a web API.

## Installation

Follow the steps below to run the project on your local machine.

**1. Clone the Repository**

git clone https://github.com/ilkerl/SimpleLibrarySystem.git

cd SimpleLibrarySystem

**2. Create a Virtual Environment (Recommended)**

Create and activate a virtual environment to isolate the project's packages from your system.


**3. Install Dependencies**

Install all the required libraries for the project using the requirements.txt file.

pip install -r requirements.txt

## Usage
The project can be run in two different ways: as a terminal application or as an API server.

**Stage 1 & 2: Terminal Application**

You can use the command-line interface to manage your books, either by adding them manually or by fetching their details from the internet using an ISBN.

To run the most up-to-date version from Stage 2:

python main.py

After running this command, you can perform operations using the menu that appears.

**Stage 3: API Server**

To run the library logic as a web service, start the Uvicorn server.

uvicorn api:app --reload

Once the server starts, the API will be accessible at http://127.0.0.1:8000.

## API Documentation
While the API server is running, you can access the interactive documentation and testing interface in your browser at http://127.0.0.1:8000/docs.

**Endpoints**

1. List All Books
Endpoint: GET /books

Description: Returns a list of all books in the library in JSON format.

Success Response (200 OK):

[
  {
    "title": "Dune",
    "author": "Frank Herbert",
    "isbn": "9780441013593"
  }
]

2. Add a Book via ISBN
Endpoint: POST /books

Description: Finds a book using the provided ISBN via the Open Library API and adds it to the library.

Request Body:

{
  "isbn": "9780743273565"
}

Success Response (201 Created): Returns the details of the added book.

3. Delete a Book
Endpoint: DELETE /books/{isbn}

Description: Deletes the book with the specified ISBN from the library.

Success Response (200 OK):

{
  "message": "Book successfully deleted",
  "isbn": "9780441013593"
}
