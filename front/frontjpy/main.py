import os
import justpy as jp

from authlib.integrations.requests_client import OAuth2Session
from dotenv import find_dotenv, load_dotenv

from views.books import Books
from views.book_form import BookForm
from views.index import Index
from views.customers import Customers
from components.base import Base
from components.router import Router

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

session_dict = {}


@jp.SetRoute('/auth/login')
async def login(request):
    if request.session_id not in session_dict:
        session_dict[request.session_id] = {}
    redirect_uri = "http://127.0.0.1:8002/auth/callback"
    client = OAuth2Session(client_id=os.environ.get("AUTH0_CLIENT_ID"),
                           client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
                           scope="openid profile email",
                           redirect_uri=redirect_uri)
    authorization_endpoint = f'https://{os.environ.get("AUTH0_DOMAIN")}/authorize'
    uri, state = client.create_authorization_url(authorization_endpoint)
    session_data = session_dict[request.session_id]
    session_data['state'] = state

    wp = jp.WebPage()
    jp.P(text="wait to redirect", a=wp)

    async def page_ready(self, msg):
        print("redirecting")
        self.redirect = uri
    wp.on("page_ready", page_ready)
    return wp


@jp.SetRoute('/auth/callback')
async def callback(request):
    redirect = "/auth/login"
    if request.session_id in session_dict and 'state' in session_dict[request.session_id]:
        session_data = session_dict[request.session_id]
        state = session_data.get('state')
        client = OAuth2Session(client_id=os.environ.get("AUTH0_CLIENT_ID"),
                               client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
                               token_endpoint_auth_method='client_secret_post',
                               state=state)

        authorization_response = request.query_params
        token_endpoint = f'https://{os.environ.get("AUTH0_DOMAIN")}/oauth/token'
        token = client.fetch_token(token_endpoint,
                                   authorization_response=authorization_response,
                                   audience="https://template-microservices/")
        session_data['token'] = token.get('access_token')
        redirect = "/"

    wp = jp.WebPage()
    jp.P(text="wait to redirect", a=wp)

    async def page_ready(self, msg):
        print("redirecting")
        self.redirect = redirect
    wp.on("page_ready", page_ready)
    return wp


@jp.SetRoute('/{path}')
def app(request):
    if request.session_id not in session_dict:
        session_dict[request.session_id] = {}
    token = session_dict[request.session_id].get('token')
    wp = Base(token=token)
    views = [View(page=wp, token=token, a=wp.content) for View in [Index, Books, BookForm, Customers]]
    router = Router(views=views, root=wp, request=request)
    wp.navbar.init_router(router)
    for view in views:
        view.use_router(router)
    wp.on("page_ready", router.current.page_ready)
    return wp


if __name__ == "__main__":
    jp.justpy(app)


