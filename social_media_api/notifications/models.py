from django.db import models

# Create your models here.

# notifications/models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    actor = models.ForeignKey(User, related_name='actor_notifications', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Generic relation to allow for notifications on different types of models (e.g., Post, Comment)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    is_read = models.BooleanField(default=False)  # To track whether the notification has been read

    def __str__(self):
        return f'Notification for {self.recipient.username}: {self.verb}'
 