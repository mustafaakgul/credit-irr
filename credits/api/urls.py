from django.urls import path
from credits.api.views import IRRTableAPIView


app_name = 'credits'


urlpatterns = [
    path('create', IRRTableAPIView.as_view(), name='create'),
]