import justpy as jp
from views.view import View


class Customers(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "customers"
        self.name = "customers-list"
        self.path = "/customers"
        self.nav = True
        root = self
        jp.P(text="customers", a=root)
