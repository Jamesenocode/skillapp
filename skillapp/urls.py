"""
URL configuration for skillapp project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

# This block allows Django to serve your CSS, images, and user-uploaded media during development
if settings.DEBUG:
    # Serves user-uploaded media (passports)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serves static assets (CSS, Carousel Images)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])