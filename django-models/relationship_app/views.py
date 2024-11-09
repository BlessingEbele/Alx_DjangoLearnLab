from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile



# Create your views here.
def list_books(request):
    books = Book.objects.all()
    # context = {'list_books': books}
    # return render(request, 'books/list_books.html', context)
    return render(request, 'relationship_app/list_books.html', {'books': books})


from django.views.generic.detail import DetailView
from .models import Library

class LibraryetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'



    from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy

# Custom registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})



# Role-checking functions
def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html', {})

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html', {})

# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html', {})
