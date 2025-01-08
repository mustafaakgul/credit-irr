from django.contrib import admin
from .models import *


@admin.register(IRRTable)
class BankAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IRRTable._meta.fields]
    list_display_links = ["initial"]
    search_fields = ["initial"]
    list_filter = ["initial"]

    class Meta:
        model = IRRTable