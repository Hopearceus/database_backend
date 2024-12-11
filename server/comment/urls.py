from . import views

from django.urls import path

urlpatterns = [
    path('list/', views.get_comments, name='get_comments'),
    path('add/', views.add_comment, name='add_comment'),
    path('delete/', views.delete_comment, name='delete_comment'),
    path('notices/', views.get_notices, name='get_notices'),
]