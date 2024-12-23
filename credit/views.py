from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import SingleTableView
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.forms import modelformset_factory

from .forms import IRRTableForm
from .models import IRRTable
from .tables import IRRTableTemp

import numpy_financial as npf


class IRRTableListView(SingleTableView):
    model = IRRTable
    table_class = IRRTableTemp
    template_name = 'indexTable.html'
    paginate_by = 100

# class IRRTableListView(ListView):
#     model = IRRTable
#     template_name = 'indexTable.html'

def index(request):
    IRRFormSet = modelformset_factory(IRRTable, form=IRRTableForm)
    formset = IRRFormSet(request.POST or None, queryset=IRRTable.objects.none())

    context = {
        'formset': formset,
    }

    if request.method == 'POST':
        if formset.is_valid():
            try:
                with transaction.atomic():
                    # logger.info("Invoice CREATED : ", request.user.username)
                    #formset.save()
                    messages.success(request, 'İşlem başarılı bir şekilde gerçekleştirildi.')


                    for form in formset:
                        irr_table_index = form.cleaned_data['index']
                        irr_table_index_type = form.cleaned_data['index_type']
                        irr_table_amount = form.cleaned_data['amount']
                        print("IRR Table Values: ", irr_table_index, irr_table_index_type, irr_table_amount)

            except IntegrityError:
                messages.error(request, "Hata oluştu. Lütfen tekrar deneyiniz.")
                # logger.error('Invoice NOT CREATED: ', request.user.username)
            except Exception as e:
                messages.error(request, "Hata oluştu. Lütfen tekrar deneyiniz.")
                # logger.error('Exception : ', e)
    return render(request, 'profile_form.html', context)


    # irr = npf.irr([-250000, 100000, 150000, 200000, 250000, 300000])
    # print("Internal rate of return: " % irr)



def calculate_irr(cash_flows):
    return npf.irr(cash_flows)

def get_cash_flows(initial_investment, cash_flows):
    if initial_investment > 0:
        initial_investment = -1 * initial_investment
    return [initial_investment] + cash_flows