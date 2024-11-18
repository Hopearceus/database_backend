from django.urls import path
from . import views

urlpatterns = [
    path('creation', views.album_creation, name='album_creation'),
    path('deletion', views.album_deletion, name='album_deletion'),
    path('add_picture', views.album_add_picture, name='album_add_picture'),
    path('detail', views.album_detail, name='album_detail')
]