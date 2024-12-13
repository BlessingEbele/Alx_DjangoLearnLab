from django.shortcuts import render

# Create your views here.
 
# notifications/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Retrieve all unread notifications for the authenticated user
        return Notification.objects.filter(recipient=self.request.user, is_read=False)

class MarkNotificationReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=404)

        # Mark the notification as read
        notification.is_read = True
        notification.save()

        return Response({"detail": "Notification marked as read."}, status=200)
