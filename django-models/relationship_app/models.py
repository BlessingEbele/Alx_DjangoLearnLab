from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name'Book')

    def __str__(self):
        return self.title


class Library(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(Book, related_name='Library')

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=50)
    library =models.OneToOneField(Library, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
