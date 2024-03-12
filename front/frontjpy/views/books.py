import asyncio
import justpy as jp
import os
import requests
from .view import View


# # @jp.SetRoute('/books')
# def books():
#     wp = Base()
#     jp.P(text="books", a=wp.content)
#     return wp


class Books(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "books"
        self.name = "books-list"
        self.path = "/books"
        self.nav = True
        root = self
        jp.P(text=self.title, a=root)
        self.container = jp.Div(a=root)
        for page in self.pages.values():
            self.container.add_page(page)
        jp.P(text="loading", a=self.container)

        def create_click(self, msg):
            if self.router:
                self.router.set_view(name='book-form')
        self.create = jp.Button(text="create", click=create_click, a=root)

    async def page_ready(self, _msg):
        if self.show:
            await self.on_show()

    async def on_show(self):
        books = self.get_books()
        self.container.delete_components()
        ul = jp.Ul(a=self.container)
        for book in books:
            li = jp.Li(text=book.get("title"), a=ul)
        await self.container.update()

    @staticmethod
    def get_books():
        endpoint = "/api/books/"
        try:
            response = requests.get(os.environ.get("API_HOST") + endpoint)
        except requests.exceptions.ConnectionError:
            return [{'title': 'connection error'}]
        data = response.json()
        return data

    def use_router(self, router):
        super().use_router(router)
        self.create.router = router
