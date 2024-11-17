from django.contrib import admin

# Register your models here.
from .models import Book

admin.site.register(Book) 

class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)