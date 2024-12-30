from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from credit_irr import settings
from credits.views import core

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("", core, name="core"),
    path("api/v1/credits/", include("credits.api.urls"), name="credits"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)