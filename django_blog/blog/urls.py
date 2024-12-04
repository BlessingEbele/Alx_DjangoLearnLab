from django.contrib.auth import Views as auth_Views 
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_Views.LoginViews.as_View(templates_name='blog/login.html'), name='login'),
    path('logout/', auth_Views.LogoutViews.as_View(templates_name='blog/logout.html'), name='logout'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'), 

]