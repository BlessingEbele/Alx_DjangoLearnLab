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
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

]