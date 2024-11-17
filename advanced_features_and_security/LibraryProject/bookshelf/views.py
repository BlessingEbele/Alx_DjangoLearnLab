from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Document

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
from bookshelf.models import Document

class EditDocumentView(PermissionRequiredMixin, UpdateView):
    model = Document
    fields = ['title', 'content']
    permission_required = 'your_app.can_edit'
