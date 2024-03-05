import justpy as jp
from views.view import View


# @jp.SetRoute('/')
# def index():
#     wp = Base()
#     jp.P(text="index", a=wp.content)
#     return wp


class Index(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "home"
        self.name = "index"
        self.path = "/"
        self.nav = True
        root = self
        jp.P(text="index", a=root)
