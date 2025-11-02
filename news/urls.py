from django.urls import path
from . import views

urlpatterns = [
    # Maps the root URL ('/') to the homepage view
    path('', views.homepage, name='homepage'),
    
    # Maps URLs like '/post/5/' to the post_detail view
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]