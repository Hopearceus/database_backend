from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_album, name='create_album'),
    path('list/', views.get_album_list, name='get_album_list'),
    path('detail/', views.get_album_detail, name='get_album_detail'),
    path('delete/', views.delete_album, name='delete_album'),
    path('photos/', views.get_album_photos, name='get_album_photos'),
    path('update/', views.update_album, name='update_album'),
    path('update/', views.update_photo_description, name='update_photo_description'),
    path('delete/', views.delete_photo, name='delete_photo'),
    path('upload/', views.upload_photos, name='upload_photos'),
    path('move/', views.move_photo_to_album, name='move_photo_to_album'),

]