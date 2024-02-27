from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from ..serializers import BookSerializer


from ..interfaces.book import BooksTestInterface as BooksInterface


books_interface = BooksInterface()


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class BookListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    serializer_class = BookSerializer
    max_words = 10

    def get_queryset(self):
        return books_interface.get_books()

    def perform_create(self, serializer):
        validated = serializer.save()
        books_interface.add_book(validated)
