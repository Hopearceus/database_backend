from django.urls import path
from . import views

urlpatterns = [
    path('creation', views.picture_upload, name='picture_upload'),
    path('deletion', views.picture_deletion, name='picture_deletion'),
    path('detail', views.picture_detail, name='picture_detail')
]