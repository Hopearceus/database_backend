from django.urls import path
from . import views

urlpatterns = [
    path('management', views.trip_management, name='trip_management'),
    path('detail', views.trip_detail, name='trip_detail'),
    path('deletion', views.trip_deletion, name='trip_deletion'),
    path('creation', views.trip_creation, name='trip_creation'),
    path('modification/description', views.trip_modification_description, name='trip_modification_description'),
    path('modification/notes', views.trip_modification_notes, name='trip_modification_notes')
]