import django_tables2 as tables
from .models import IRRTable


class IRRTableTemp(tables.Table):
    class Meta:
        model = IRRTable
        template_name = 'django_tables2/bootstrap.html'
        fields = ("index", )
