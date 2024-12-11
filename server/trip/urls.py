from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_trip, name='create_trip'),
    path('detail/', views.trip_detail, name='trip_detail'),
    path('delete/', views.delete_trip, name='delete_trip'),
    path('list/', views.get_trip_list, name='get_trip_list'),
    path('update/', views.update_trip, name='update_trip'),
    path('record/', views.add_trip_record, name='add_trip_record'),
    path('record/delete/', views.delete_trip_record, name='delete_trip_record'),
    path('record/detail/', views.get_record_detail, name='get_record_detail'),
    path('record/update/', views.update_record, name='update_record'),
    path('records/', views.get_record_list, name='get_record_list'),
]