from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from . import views
from .views import PostLikeView, PostUnlikeView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.user_feed, name='user_feed'),

    # posts/urls.py
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='like_post'),
    path('posts/<int:pk>/unlike/', PostUnlikeView.as_view(), name='unlike_post'),
]