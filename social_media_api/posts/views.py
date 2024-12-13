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



# posts/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Post, Like
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class PostLikeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=pk)  # Use get_object_or_404 to retrieve the post or raise a 404 if not found

        # Prevent the user from liking the post again
        like, created = Like.objects.get_or_create(user=user, post=post)  # get_or_create ensures no duplicate likes

        if not created:
            return Response({"detail": "You have already liked this post."}, status=400)

        # Create a notification for the post author
        notification_verb = f'{user.username} liked your post'
        notification = Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb=notification_verb,
            target=post,
            target_content_type=ContentType.objects.get_for_model(Post)
        )

        return Response({"detail": "Post liked successfully"}, status=201)

class PostUnlikeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=pk)  # Use get_object_or_404 to retrieve the post or raise a 404 if not found

        # Prevent the user from unliking a post they haven't liked
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post."}, status=400)

        # Remove the like
        like.delete()

        return Response({"detail": "Post unliked successfully"}, status=204)


# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework.exceptions import NotFound
# from .models import Post, Like
# from .serializers import PostSerializer
# from notifications.models import Notification
# from django.contrib.contenttypes.models import ContentType

# class PostLikeView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, pk, *args, **kwargs):
#         user = request.user
#         try:
#             post = Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise NotFound('Post not found')

#         # Prevent the user from liking the post again
#         if Like.objects.filter(user=user, post=post).exists():
#             return Response({"detail": "You have already liked this post."}, status=400)

#         # Create a like
#         like = Like.objects.create(user=user, post=post)

#         # Create a notification for the post author
#         notification_verb = f'{user.username} liked your post'
#         notification = Notification.objects.create(
#             recipient=post.author,
#             actor=user,
#             verb=notification_verb,
#             target=post,
#             target_content_type=ContentType.objects.get_for_model(Post)
#         )

#         return Response({"detail": "Post liked successfully"}, status=201)

# class PostUnlikeView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, pk, *args, **kwargs):
#         user = request.user
#         try:
#             post = Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise NotFound('Post not found')

#         # Prevent the user from unliking a post they haven't liked
#         like = Like.objects.filter(user=user, post=post).first()
#         if not like:
#             return Response({"detail": "You have not liked this post."}, status=400)

#         # Remove the like
#         like.delete()

#         return Response({"detail": "Post unliked successfully"}, status=204)

