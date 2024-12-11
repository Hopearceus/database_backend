from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import settings

urlpatterns = [
    path('admin', admin.site.urls),
    path('person/', include('person.urls')),
    path('trip/', include('trip.urls')),
    path('album/', include('album.urls')),
    path('entry/', include('entry.urls')),
    path('moment/', include('moment.urls')),
    path('picture', include('picture.urls')),
    path('comment', include('comment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)