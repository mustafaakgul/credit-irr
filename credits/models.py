from django.db.models import Model, FloatField, IntegerField, CharField, ForeignKey, CASCADE
from django.db import models


class IRRTable(Model):
    initial = FloatField()
    credits = models.JSONField(blank=True, default=list)

class Financial(Model):
    total_amount = CharField(max_length=100)
