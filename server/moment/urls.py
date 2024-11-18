from . import views

from django.urls import path

urlpattern = [
    path('creation', views.moment_creation, name='moment_creation'),
    path()
]