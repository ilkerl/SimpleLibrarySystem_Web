# test_api.py

from fastapi.testclient import TestClient
from api import app
import pytest

client = TestClient(app)


def test_get_all_books(mocker):
    """Test the GET /books endpoint."""
    # Kütüphanenin list_books metodunu taklit ediyoruz (mocking)
    mocker.patch('api.lib.list_books', return_value=[
        {"title": "Test Book 1", "author": "Author 1", "isbn": "111"}
    ])

    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == [
        {"title": "Test Book 1", "author": "Author 1", "isbn": "111"}
    ]


def test_add_book_success(mocker):
    """Test the POST /books endpoint for a successful case."""
    mock_book = {"title": "New Book", "author": "New Author", "isbn": "12345"}
    mocker.patch('api.lib.add_book', return_value=mock_book)

    response = client.post("/books", json={"isbn": "12345"})
    assert response.status_code == 201
    assert response.json() == mock_book


def test_add_book_not_found(mocker):
    """Test the POST /books endpoint when the book is not found."""
    mocker.patch('api.lib.add_book', return_value=None)

    response = client.post("/books", json={"isbn": "00000"})
    assert response.status_code == 404


def test_delete_book_success(mocker):
    """Test the DELETE /books/{isbn} endpoint for a successful case."""
    mocker.patch('api.lib.remove_book', return_value=True)

    response = client.delete("/books/123")
    assert response.status_code == 200
    assert response.json()["message"] == "Book successfully deleted"


def test_delete_book_not_found(mocker):
    """Test the DELETE /books/{isbn} endpoint when the book is not found."""
    mocker.patch('api.lib.remove_book', return_value=False)

    response = client.delete("/books/999")
    assert response.status_code == 404
