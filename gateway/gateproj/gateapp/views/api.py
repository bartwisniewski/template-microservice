from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from ..serializers import BookSerializer

from ..interfaces.book import book_interface


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class BookListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    serializer_class = BookSerializer
    max_words = 10

    def get_queryset(self):
        return book_interface.get_books()

    def perform_create(self, serializer):
        validated = serializer.save()
        return book_interface.add_book(validated)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        api_response = self.perform_create(serializer)
        if status.is_success(api_response.status_code):
            headers = self.get_success_headers(serializer.data)
            return Response(api_response.json(), status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=api_response.status_code)
