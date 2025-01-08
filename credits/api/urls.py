from django.urls import path
from credits.api.views import IRRTableIRRAPIView, IRRTableTableAPIView


app_name = 'credits'


urlpatterns = [
    path('create/irr', IRRTableIRRAPIView.as_view(), name='irr'),
    path('create/table', IRRTableTableAPIView.as_view(), name='table'),
]