from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    year: int


@app.get("/")
def read_root():
    return {"API Name": "Books"}


@app.get("/books/")
def read_books() -> list[Book]:
    return [Book(title="book1", author="author1", year=1888),
            Book(title="book2", author="author2", year=1989),
            Book(title="book3", author="author3", year=2015)]


@app.post("/books/")
def create_book(book: Book) -> Book:
    return book

