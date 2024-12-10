from django.urls import path
from . import views

urlpatterns = [
    path('trip/create', views.create_trip, name='create_trip'),
    path('trip/detail', views.trip_detail, name='trip_detail'),
    path('trip/delete', views.delete_trip, name='delete_trip'),
    path('trip/list', views.get_trip_list, name='get_trip_list'),
    path('trip/update', views.update_trip, name='update_trip'),
    path('trip/record', views.add_trip_record, name='add_trip_record'),
    path('trip/record/delete', views.delete_trip_record, name='delete_trip_record'),
    path('record/detail', views.get_record_detail, name='get_record_detail'),
    path('trip/record/update', views.update_record, name='update_record'),
]