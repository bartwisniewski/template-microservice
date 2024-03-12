import justpy as jp
from .navbar import Navbar


class Base(jp.WebPage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = self
        self.token = kwargs.get('token')
        self.navbar = Navbar(a=root, token=self.token)
        self.content = jp.Div(classes="flex flex-col justify-center items-center", a=root)
        self.footer = jp.Div(a=root)
        self.body_classes = "h-full"
