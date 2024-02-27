from django.urls import path

from .views import auth, web, api

urlpatterns = [
    path("", web.IndexView.as_view(), name="index"),
    path("login", auth.login, name="login"),
    path("logout", auth.logout, name="logout"),
    path("callback", auth.callback, name="callback"),
    path("books/", web.BookListView.as_view(), name="books"),
    path("create/", web.BookCreateView.as_view(), name="book-create"),
    path("api/books/", api.BookListView.as_view(), name="api-books"),
]
