from django.urls import path
from . import views

urlpatterns = [
    path('creation', views.entry_creation, name='entry_creation'),
    path('deletion', views.entry_deletion, name='entry_deletion'),
    path('modification', views.entry_modification, name='entry_modification'),
    path('detail', views.entry_detail, name='entry_detail')
]