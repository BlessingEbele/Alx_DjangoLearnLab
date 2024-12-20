from django.db import models
from .views import filters

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


"""
Author model represents authors in the system.
Book model represents books written by authors. Each book links to one author.
"""
