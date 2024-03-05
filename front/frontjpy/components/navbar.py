import justpy as jp


class Navbar(jp.Div):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_classes("flex flex-row justify-between gap-2 bg-gray-100 mb-8")
        root = self
        self.start = jp.Div(a=root)
        self.middle = jp.Div(a=root, classes="flex flex-row justify-center gap-2")
        self.end = jp.Div(a=root, classes="mr-8")
        if not kwargs.get('token'):
            jp.A(text="login", href="/auth/login", a=self.end)
        else:
            jp.A(text="logout", href="/auth/logout", a=self.end)

    def init_router(self, router):
        for view in router.views.values():
            if view.nav:
                router.button_from_view(view=view, root=self.middle)
