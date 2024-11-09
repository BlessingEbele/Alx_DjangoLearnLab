from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver


# Create your models here.


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE#, related_name'Book')

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


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),

    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Automatically create a UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


#adding custom permission

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

    def __str__(self):
        return self.title
