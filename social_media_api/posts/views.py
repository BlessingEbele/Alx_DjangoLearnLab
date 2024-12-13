from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


from django_filters.rest_framework import DjangoFilterBackend

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PostSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    followed_users = request.user.following.all()
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from django.contrib.auth.models import User

class PostListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensures only authenticated users can access the view

    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of posts from users that the authenticated user is following.
        """
        # Retrieve the authenticated user
        user = request.user
        
        # Get the list of users that the authenticated user is following
        following_users = user.following.all()  # Assuming there's a `following` relationship defined on the user model

        # Filter posts by those authors the user is following
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')  # Adjust order as needed

        # Serialize the data
        serializer = PostSerializer(posts, many=True)
        
        # Return the serialized data
        return Response(serializer.data)
