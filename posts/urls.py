from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='view'),
    path('add_post', views.addPost, name='add_post'),
    path('posts', views.posts, name='posts'),
    path('post/<str:pk>', views.post, name='post'),
    path('like/<str:pk>', views.like, name='like')
]
