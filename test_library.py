# test_library.py

import pytest
import os
import httpx
from library import Library
from book import Book


@pytest.fixture
def library_fixture():
    test_filename = "test_library.json"
    lib = Library(filename=test_filename)
    yield lib
    if os.path.exists(test_filename):
        os.remove(test_filename)


def test_add_book_from_api_success(library_fixture, mocker):
    """
    Tests successfully adding a book by mocking a successful API response.
    """
    isbn = "9780345339683"
    mock_api_response = {
        f"ISBN:{isbn}": {
            "title": "The Hobbit",
            "authors": [{"name": "J.R.R. Tolkien"}]
        }
    }
    mock_response = httpx.Response(
        200,
        json=mock_api_response,
        request=httpx.Request("GET", "https://test.url")
    )
    mocker.patch("httpx.get", return_value=mock_response)

    added_book = library_fixture.add_book(isbn)

    assert added_book is not None
    assert len(library_fixture.books) == 1
    assert library_fixture.books[0].title == "The Hobbit"


def test_add_book_from_api_not_found(library_fixture, mocker):
    """
    Tests the case where the API cannot find a book (404).
    """
    isbn = "0000000000000"
    mock_response = httpx.Response(
        404,
        request=httpx.Request("GET", "https://test.url")
    )
    mocker.patch("httpx.get", return_value=mock_response)

    added_book = library_fixture.add_book(isbn)

    assert added_book is None
    assert len(library_fixture.books) == 0
