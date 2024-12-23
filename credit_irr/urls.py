# from django.contrib import admin
from django.urls import path
from credit.views import index, IRRTableListView

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path("table/", IRRTableListView.as_view(), name="table"),

]
