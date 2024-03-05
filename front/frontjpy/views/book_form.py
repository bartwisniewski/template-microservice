import justpy as jp
import os
import requests
from views.view import View


def url():
    host = os.environ.get("API_HOST")
    port = os.environ.get("API_PORT")
    return f"http://{host}:{port}"


button_classes = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2'
input_classes = 'border m-2 p-2'


class BookForm(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "create book"
        self.name = "book-form"
        self.path = "/book-create"
        self.nav = False
        root = self
        self.form1 = jp.Form(a=root, classes='border m-1 p-1 w-64')
        title_label = jp.Label(text='Title',
                               classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=self.form1)
        in1 = jp.Input(name='title', placeholder='Title', a=self.form1, classes='form-input')
        title_label.for_component = in1

        author_label = jp.Label(text='Author',
                               classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=self.form1)
        in2 = jp.Input(name='author', placeholder='Author', a=self.form1, classes='form-input')
        author_label.for_component = in2

        year_label = jp.Label(text='Year',
                               classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=self.form1)
        in3 = jp.Input(name='year', placeholder='Year', a=self.form1, classes='form-input')
        year_label.for_component = in3

        submit_button = jp.Input(value='Submit Form', type='submit', a=self.form1, classes=button_classes)

        root = self

        def submit_form(self, msg):
            data = {}
            for field in msg.form_data:
                if field.type != 'submit':
                    print(field)
                    print(field.name)
                    print(field.value)
                    data[field.name] = field.value
            ok, errors = BookForm.submit_book(data=data, token=root.token)
            if ok:
                self.router.set_view(name='books-list')
            else:
                print(errors)
        self.form1.on('submit', submit_form)

    @staticmethod
    def submit_book(data, token):
        endpoint = "/api/books/"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url() + endpoint, json=data, headers=headers)
        if response.status_code == 201:
            return True, None
        errors = response.json()
        return False, errors

    def use_router(self, router):
        super().use_router(router)
        self.form1.router = router
