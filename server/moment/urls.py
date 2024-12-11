from . import views

from django.urls import path

urlpatterns = [
    path('add/', views.add_moment, name='add_moment'),
    path('delete/', views.delete_moment, name='delete_moment'),
    path('list/', views.get_moments, name='get_moments'),
    path('detail/', views.get_moment_detail, name='get_moment_detail'),
    path('discover/', views.get_discover_moments, name='get_discover_moments'),
    path('add_picture/<int:mid>/<int:pid>/', views.moment_add_picture, name='moment_add_picture'),
    path('discover/', views.get_discover_moments, name='get_discover_moments'),
    path('search/', views.search_moment, name='search_moment'),
    path('num/', views.moment_num, name='moment_num'),
]