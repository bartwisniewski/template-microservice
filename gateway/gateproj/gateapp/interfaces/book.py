import dataclasses


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
