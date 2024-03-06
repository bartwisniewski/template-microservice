import justpy as jp


class View(jp.Div):
    def __init__(self, page, token,  **kwargs):
        super().__init__(**kwargs)
        self.title = "title"
        self.name = "name"
        self.path = "path"
        self.show = False
        self.token = token
        self.router = None
        self.add_page(page)

    def set_show(self):
        self.show = True
        jp.run_task(self.on_show())

    async def page_ready(self, _msg):
        pass

    async def on_show(self):
        pass

    def use_router(self, router):
        self.router = router
