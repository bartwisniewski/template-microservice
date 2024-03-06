import dataclasses
import os
import requests

from ..serializers import BookSerializer


@dataclasses.dataclass
class Book:
    title: str
    author: str
    year: int


class BooksTestInterface:
    def __init__(self):
        self.books = [Book("book1", "author1", 1888), Book("book2", "author2", 1989), Book("book3", "author3", 2015)]

    def get_books(self) -> list[Book]:
        return self.books

    def add_book(self, book_data: dict):
        book = Book(**book_data)
        self.books.append(book)
        return True


class BooksServiceInterface:
    Serializer = BookSerializer

    def __init__(self):
        self.url = os.environ.get("BOOKS_HOST", None)

    def get_books(self) -> list[Book]:
        endpoint = "/books/"
        response = requests.get(self.url + endpoint)
        data = response.json()
        serializer = self.Serializer(data=data, many=True)
        serializer.is_valid()
        return serializer.validated_data

    def add_book(self, book_data: dict):
        endpoint = "/books/"
        response = requests.post(self.url + endpoint, json=book_data)
        return response


book_interface = BooksServiceInterface()
