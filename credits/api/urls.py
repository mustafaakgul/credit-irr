from django.urls import path
from credits.api.views import IRRTableTableAPIView


app_name = 'credits'


urlpatterns = [
    path('create/table', IRRTableTableAPIView.as_view(), name='table'),
]