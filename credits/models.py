from django.db.models import Model, FloatField, IntegerField, CharField, ForeignKey, CASCADE
from django.db import models


class IRRTable(Model):
    initial = FloatField()
    credits = models.JSONField(blank=True, default=list)

class Financial(Model):
    total_amount = CharField(max_length=100)

class CreditTable(Model):
    credit_amount = FloatField()
    interest = FloatField()
    tax = FloatField()
    principal_amount = FloatField()
    remaining_principal_amount = FloatField()