from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from rest_framework import status

from .auth import OAuthSessionMixin
from ..forms import BookForm
from ..interfaces.book import book_interface
from ..serializers import BookSerializer


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
        return book_interface.get_books()


class BookCreateView(OAuthSessionMixin, FormView):
    """
    This View creates entry
    """

    template_name = "gateapp/book_form.html"
    form_class = BookForm
    success_url = reverse_lazy("books")
    redirect_url = reverse_lazy("books")

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(form=form)
        if 'api_error' in kwargs:
            context['api_error'] = kwargs['api_error']
        return self.render_to_response(context)

    def form_valid(self, form):
        serializer = BookSerializer(data=form.cleaned_data)
        serializer.is_valid()
        api_response = book_interface.add_book(serializer.data)
        if status.is_success(api_response.status_code):
            return super().form_valid(form)
        return self.form_invalid(form=form, api_error=api_response.reason)
