from django.db import models

class IRRTable(models.Model):
    index = models.IntegerField()
    index_type = models.CharField(max_length=30)
    amount = models.FloatField()
