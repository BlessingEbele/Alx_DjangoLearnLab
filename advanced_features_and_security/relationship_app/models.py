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




#started from here
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        permissions = [
            ("can_view", "Can view documents"),
            ("can_create", "Can create documents"),
            ("can_edit", "Can edit documents"),
            ("can_delete", "Can delete documents"),
        ]



from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from your_app.models import Document

content_type = ContentType.objects.get_for_model(Document)

permissions = {
    "Editors": ["can_edit", "can_create"],
    "Viewers": ["can_view"],
    "Admins": ["can_view", "can_create", "can_edit", "can_delete"],
}

for group_name, perms in permissions.items():
    group, created = Group.objects.get_or_create(name=group_name)
    for perm in perms:
        permission = Permission.objects.get(codename=perm, content_type=content_type)
        group.permissions.add(permission)







from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('your_app.can_edit', raise_exception=True)
def edit_document(request, document_id):
    # Logic to edit the document
    pass






from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import UpdateView
from your_app.models import Document

class EditDocumentView(PermissionRequiredMixin, UpdateView):
    model = Document
    fields = ['title', 'content']
    permission_required = 'your_app.can_edit'





#markdown document
# Permissions and Groups in Django
- `can_view`: Permission to view documents.
- `can_create`: Permission to create documents.
- `can_edit`: Permission to edit documents.
- `can_delete`: Permission to delete documents.

## Groups
- **Editors**: can_edit, can_create
- **Viewers**: can_view
- **Admins**: All permissions

