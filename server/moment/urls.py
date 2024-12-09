from . import views

from django.urls import path

urlpatterns = [
    path('comment/list/', views.get_comments, name='get_comments'),
    path('comment/add/', views.add_comment, name='add_comment'),
    path('comment/delete/', views.delete_comment, name='delete_comment'),
    path('add/', views.add_moment, name='add_moment'),
    path('delete/', views.delete_moment, name='delete_moment'),
    path('list/', views.get_moments, name='get_moments'),
    path('detail/', views.get_moment_detail, name='get_moment_detail'),
    path('discover/', views.get_discover_moments, name='get_discover_moments'),
    path('add_picture/<int:mid>/<int:pid>/', views.moment_add_picture, name='moment_add_picture'),
    path('discover/', views.get_discover_moments, name='get_discover_moments'),
]