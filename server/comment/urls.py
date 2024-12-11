from . import views

from django.urls import path

urlpatterns = [
    path('comment/list/', views.get_comments, name='get_comments'),
    path('comment/add/', views.add_comment, name='add_comment'),
    path('comment/delete/', views.delete_comment, name='delete_comment'),
    path('comment/notices/', views.get_notices, name='get_notices'),
]