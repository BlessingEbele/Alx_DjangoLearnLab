from django.shortcuts import render

# Create your views here.

# Create your views here.
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.BookViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



#just strated here now 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class BookListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly,IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class UserListView(generics.ListAPIView):
    ...
    filter_backends = [DjangoFilterBackend]

