from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from .auth import OAuthSessionMixin
from ..forms import BookForm
from ..interfaces.book import BooksTestInterface as BooksInterface


books_interface = BooksInterface()


class IndexView(TemplateView):
    template_name = "gateapp/index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["session"] = request.session.get("user")
        return self.render_to_response(context)


class BookListView(ListView):
    """
    Entry list view with pagination
    """

    template_name = "gateapp/book_list.html"
    paginate_by = 10

    def get_queryset(self):
        return books_interface.get_books()


class BookCreateView(OAuthSessionMixin, FormView):
    """
    This View creates entry
    """

    template_name = "gateapp/book_form.html"
    form_class = BookForm
    success_url = reverse_lazy("books")
    redirect_url = reverse_lazy("books")

    def form_valid(self, form):
        books_interface.add_book(form.cleaned_data)
        return super().form_valid(form)
