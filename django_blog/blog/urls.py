from django.contrib.auth import Views as auth_Views 
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_Views.LoginViews.as_View(templates_name='blog/login.html'), name='login'),
    path('logout/', auth_Views.LogoutViews.as_View(templates_name='blog/logout.html'), name='logout'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'), 
    
    path('', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),



    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),
    path('search/', views.search_posts, name='search_posts'),
]
