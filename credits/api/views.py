from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core import serializers

from rest_framework.views import APIView

from credits.api.serializers import IRRCreditCreateSerializer
from credits.models import IRRTable, CreditTable, ResponseModel
from credits.utils.irr_func import get_irr, calculate_interest, calculate_tax, calculate_prn, calculate_rm_prn, \
    get_credit_type, get_consumer_credit_type, calculate_interest_of_credit_blockage, transform, sum_of_total_cost, \
    get_irr_ivo

import os


class IRRTableGenericAPIView(CreateAPIView):
    queryset = IRRTable.objects.all()
    serializer_class = IRRCreditCreateSerializer
    permission_classes = [AllowAny]


class GetLocale(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        res1 = os.popen("locale -a")
        res2 = os.popen("export LC_ALL=\"en_US.UTF-8\"")
        res3 = os.popen("export LC_CTYPE=\"en_US.UTF-8\"")
        #res34 = os.popen("sudo apt-get install language-pack-tr")
        res4 = os.popen("sudo dpkg-reconfigure locales")
        res5 = os.popen("locale -a")
        return Response({"result": res5}, status=status.HTTP_200_OK)


class IRRTableTableAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = IRRCreditCreateSerializer(data=request.data)
        if serializer.is_valid():
            resp = ResponseModel()

            # Define Variables
            cash_flows = []
            credit_table_list = []

            # Investment Values
            initial_investment = serializer.data['initial']
            current_amount = initial_investment

            # Credits
            credits = serializer.data['credits']

            # Credit Type
            credit_type = serializer.data['credit_type']

            # Consumer Credit Type
            consumer_credit_type = serializer.data['consumer_credit_type']

            # Expenses
            expenses = serializer.data['expenses']
            total_expense = 0

            # Block Variables
            block_day = serializer.data['block']
            block_amount = 0
            if (block_day > 0):
                block_amount = initial_investment

            # Tax Rates
            taxes = serializer.data['taxes']
            tax_bsmv = next((float(sub['amount']) for sub in taxes if sub['title'] == "BSMV" and sub['id'] == 0), 0)
            tax_kkdf = next((float(sub['amount']) for sub in taxes if sub['title'] == "KKDF" and sub['id'] == 1), 0)

            # Validations
            if (len(credits) == 0):
                return Response({"error": "Kredi Tutarı boş olamaz."}, status=status.HTTP_400_BAD_REQUEST)

            _credit_type = get_credit_type(credit_type)
            if (_credit_type == 0):
                return Response({"error": "Kredi Türü hatalı."}, status=status.HTTP_400_BAD_REQUEST)

            _consumer_credit_type = get_consumer_credit_type(consumer_credit_type)
            if (_consumer_credit_type == 0):
                return Response({"error": "Bireysel Kredi Türü hatalı."}, status=status.HTTP_400_BAD_REQUEST)

            if (initial_investment < 0):
                return Response({"error": "Kredi Tutarı eksi bir değer olamaz."}, status=status.HTTP_400_BAD_REQUEST)

            # Calculations
            for expense in expenses:
                if (expense['amount']):
                    total_expense += float(expense['amount'])

            base_investment = initial_investment - total_expense

            for credit in credits:
                cash_flows.append(credit)
            irr = get_irr(float(base_investment), cash_flows)     # IRR ITFA
            irr_ivo = get_irr_ivo(float(base_investment), cash_flows, block_amount, block_day, total_expense) # IRR IVO
            irr_str = "% {}".format(round(irr * 100, 2))
            irr_ivo_str = "% {}".format(round(irr_ivo * 100, 2))
            irr_ivo_year = (pow((1 + irr_ivo), 12) -1)

            sum_of_interest = 0
            sum_of_tax = 0
            interest_credit_blockage = calculate_interest_of_credit_blockage(block_amount, block_day, irr)

            for credit in credits:
                #current_amount = initial_investment
                _interest = calculate_interest(current_amount, irr, tax_bsmv, tax_kkdf)
                _tax = calculate_tax(_interest, tax_bsmv, tax_kkdf)
                _principal_amount = calculate_prn(credit, _interest, _tax)
                _remaining_principal_amount = calculate_rm_prn(current_amount, _principal_amount)

                sum_of_interest += _interest
                sum_of_tax += _tax

                credit_table = CreditTable(
                    credit_amount=transform(credit),
                    interest=transform(_interest),
                    tax=transform(_tax),
                    principal_amount=transform(_principal_amount),
                    remaining_principal_amount=transform(_remaining_principal_amount)
                    )
                credit_table_list.append(credit_table)
                current_amount = _remaining_principal_amount

            all_expenses_title = "Peşin Ödenen Masraflar (Vergiler Dahil)"
            _prepaid_expenses = total_expense
            _interest_payable_on_loans = sum_of_interest
            _taxes_on_loan_interest_payable = sum_of_tax
            _interest_cost_related_to_loan_blockage = interest_credit_blockage
            _total_cost = 0
            _monthly_cost_ivo = irr_ivo_str
            _annual_compound_cost_ivo = "% {}".format(round(irr_ivo_year * 100, 2))
            table = credit_table_list

            data_irr = {
                "irr": irr_str,
                "table": serializers.serialize('json', table),
                "prepaid_expenses": transform(_prepaid_expenses),
                "interest_payable_on_loans": transform(_interest_payable_on_loans),
                "taxes_on_loan_interest_payable": transform(_taxes_on_loan_interest_payable),
                "interest_cost_related_to_loan_blockage": transform(_interest_cost_related_to_loan_blockage),
                "total_cost": transform(sum_of_total_cost(
                    _prepaid_expenses,
                    _interest_payable_on_loans,
                    _taxes_on_loan_interest_payable,
                    _interest_cost_related_to_loan_blockage
                )),
                "monthly_cost_ivo": _monthly_cost_ivo,
                "annual_compound_cost_ivo": _annual_compound_cost_ivo
            }
            response = Response(data=data_irr, status=status.HTTP_200_OK)

            return response
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)