import justpy as jp


class Router:
    def __init__(self, views, root, request):
        self.views = Router.views_to_dict(views)
        self.root = root
        self.request = request
        self.current = self.by_path(self.request['path'])
        if self.current:
            self.current.set_show()

    def set_view(self, **kwargs):
        view = None
        if 'path' in kwargs:
            view = self.by_path(kwargs['path'])
        elif 'name' in kwargs:
            view = self.by_name(kwargs['name'])
        if not view:
            return self.current

        if self.current:
            self.current.show = False
        view.set_show()
        self.current = view
        self.root.display_url = view.path

    def by_path(self, path):
        for name, view in self.views.items():
            if view.path == path:
                return view
        return None

    def by_name(self, name):
        return self.views.get(name)

    @staticmethod
    def views_to_dict(views):
        views_dict = {}
        for view in views:
            views_dict[view.name] = view
        return views_dict

    def button_from_view(self, view, root):
        b = jp.Button(text=view.title, a=root)
        router = self

        def on_click(button, msg):
            router.set_view(name=button.view_name)
        b.view_name = view.name
        b.on('click', on_click)
        return b
