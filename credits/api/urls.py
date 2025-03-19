from django.urls import path
from credits.api.views import IRRTableTableAPIView, GetLocale


app_name = 'credits'


urlpatterns = [
    path('create/table', IRRTableTableAPIView.as_view(), name='table'),
    path('get/locale', GetLocale.as_view(), name='get-locale'),
]