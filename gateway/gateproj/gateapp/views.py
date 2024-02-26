from authlib.integrations.django_client import OAuth
from urllib.parse import quote_plus, urlencode

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from .interfaces.book import BooksTestInterface as BooksInterface
from .forms import BookForm


oauth = OAuth()
books_interface = BooksInterface()


oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token

    return redirect(request.build_absolute_uri(reverse("index")))


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


class IndexView(TemplateView):
    template_name = "gateapp/index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["session"] = request.session.get("user")
        return self.render_to_response(context)


class OAuthSessionMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("user"):
            return HttpResponseRedirect(reverse_lazy("index"))
        return super().dispatch(request, *args, **kwargs)


class BookListView(ListView):
    """
    Entry list view with pagination
    """

    template_name = "gateapp/book_list.html"
    paginate_by = 10

    def get_queryset(self):
        return books_interface.get_books()


class BookCreateView(FormView):
    """
    This View creates entry
    """

    template_name = "gateapp/book_form.html"
    form_class = BookForm
    success_url = reverse_lazy("books")

    def form_valid(self, form):
        books_interface.add_book(form.cleaned_data)
        return super().form_valid(form)
