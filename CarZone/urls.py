from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns: list = [
    path('admin/', admin.site.urls),
    path('', include('CarZone.accounts.urls')),
    path('car/', include('CarZone.car.urls')),
    path('api/', include('CarZone.api.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
