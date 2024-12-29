from django.shortcuts import render
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.forms import modelformset_factory

from .forms import IRRTableForm, FinancialForm
from .models import IRRTable
from .utils.irr_func import get_irr


def  core(request):
    IRRTableFormset = modelformset_factory(IRRTable, form=IRRTableForm)
    formset = IRRTableFormset(request.POST or None, queryset=IRRTable.objects.none(), prefix='irrtable')
    context = {
        'formset': formset,
    }

    if request.method == 'POST':
        if formset.is_valid():
            try:
                initial_investment = request.POST.get('initial-investment')
                with transaction.atomic():
                    cash_flows = []
                    for form in formset:
                        irr_table_index = form.cleaned_data['index']
                        irr_table_amount = form.cleaned_data['amount']
                        cash_flows.append(irr_table_amount)
                        print("IRR Table Values: ", irr_table_index, irr_table_amount)
                    irr = get_irr(float(initial_investment), cash_flows)
                    print(irr)
                    # logger.info("IRR Created : ", irr)
                messages.success(request, 'İşlem başarılı bir şekilde gerçekleştirildi.')
            except IntegrityError:
                # logger.error('Error Occured: IntegrityError')
                messages.error(request, "Hata oluştu. Lütfen tekrar deneyiniz.")
            except Exception as ex:
                # logger.error('Error Occured: ', ex)
                messages.error(request, "Hata oluştu. Lütfen tekrar deneyiniz.")

    return render(request, 'core.html', context)
