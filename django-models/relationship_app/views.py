from django.shortcuts import render
from .models import Book


# Create your views here.
def list_books(request):
    books = Book.objects.all()
    # context = {'list_books': books}
    # return render(request, 'books/list_books.html', context)
    return render(request, 'relationship_app/list_books.html', {'books': books})


from django.views.generic import DetailView
from .models import Library

class LibraryetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'