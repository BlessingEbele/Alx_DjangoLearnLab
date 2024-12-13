from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#follow management this will enable users to foloow and unfollow other users 

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    if target_user == request.user:
        return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    request.user.following.add(target_user)
    return Response({"message": f"You are now following {target_user.username}"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    request.user.following.remove(target_user)
    return Response({"message": f"You have unfollowed {target_user.username}"}, status=status.HTTP_200_OK)


lass UserProfileView(APIView):
    """
    Handles retrieving and updating user profiles.
    """

    def get(self, request, username=None):
        if username:
            try:
                user = CustomUser.objects.get(username=username)
                serializer = CustomUserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, username=None):
        if username:
            try:
                user = CustomUser.objects.get(username=username)
                serializer = CustomUserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(APIView):
    """
    Handles following another user.
    """

    def post(self, request, username=None):
        if username:
            try:
                user_to_follow = CustomUser.objects.get(username=username)
                if user_to_follow == request.user:
                    return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
                request.user.following.add(user_to_follow)
                return Response({"success": f"You are now following {username}."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)


class UnfollowUserView(APIView):
    """
    Handles unfollowing another user.
    """

    def post(self, request, username=None):
        if username:
            try:
                user_to_unfollow = CustomUser.objects.get(username=username)
                if user_to_unfollow == request.user:
                    return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
                request.user.following.remove(user_to_unfollow)
                return Response({"success": f"You have unfollowed {username}."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensures only authenticated users can access this view

    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of all users.
        Only authenticated users can access this endpoint.
        """
        users = CustomUser.objects.all()  # Retrieves all CustomUser objects
        serializer = CustomUserSerializer(users, many=True)  # Serialize the data
        return Response(serializer.data)
