from . import views

from django.urls import path

urlpattern = [
    path('creation', views.moment_creation, name='moment_creation'),
    path('deletion', views.moment_deletion, name='moment_deletion'),
    path('detail', views.moment_detail, name='moment_detail'),
    path('trip_share', views.trip_share, name='trip_share'),
    path('comment', views.moment_comment, name='moment_comment'),
    path('add_picture', views.moment_add_picture, name='moment_add_picture')
]