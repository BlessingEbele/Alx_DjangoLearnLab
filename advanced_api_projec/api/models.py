from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    publication_year = models.IntegerField(unique_for_year=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='Books')

    def __str__(self):
        return self.title