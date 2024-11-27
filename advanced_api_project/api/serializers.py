from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class meta:
        model = Author 
        fields =  ['id', 'content', 'author', 'author_name', 'created_at']


