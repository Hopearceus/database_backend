from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin', admin.site.urls),
    path('person/', include('person.urls')),
    path('trip/', include('trip.urls')),
    path('album/', include('album.urls')),
    path('entry/', include('entry.urls')),
    path('moment/', include('moment.urls')),
]