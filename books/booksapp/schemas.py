from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    year: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class ConfigDict:
        from_attributes = True
