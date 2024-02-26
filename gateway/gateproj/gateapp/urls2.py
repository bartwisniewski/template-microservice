from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("create/", views.BookCreateView.as_view(), name="book-create"),
]
