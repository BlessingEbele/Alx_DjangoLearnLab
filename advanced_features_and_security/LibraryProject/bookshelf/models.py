from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()


    from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)




class CustomUser(AbstractUser):
    ...
    objects = CustomUserManager()


from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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

