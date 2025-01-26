from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core import serializers

from rest_framework.views import APIView

from credits.api.serializers import IRRCreditCreateSerializer
from credits.models import IRRTable, CreditTable, ResponseModel
from credits.utils.irr_func import get_irr, calculate_interest, calculate_tax, calculate_prn, calculate_rm_prn, \
    get_credit_type, get_consumer_credit_type


class IRRTableGenericAPIView(CreateAPIView):
    queryset = IRRTable.objects.all()
    serializer_class = IRRCreditCreateSerializer
    permission_classes = [AllowAny]

class IRRTableIRRAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = IRRCreditCreateSerializer(data=request.data)
        if serializer.is_valid():
            cash_flows = []
            initial_investment = serializer.data['initial']
            credits = serializer.data['credits']

            for credit in credits:
                cash_flows.append(credit)

            irr = get_irr(float(initial_investment), cash_flows)
            data_irr = {"irr": irr}
            response = Response(data=data_irr, status=status.HTTP_200_OK)

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

            # Tax Rates
            taxes = serializer.data['taxes']
            tax_bsmv = next((sub for sub in taxes if sub['title'] == "BSMV" and sub['id'] == 0), 0)
            tax_kkdf = next((sub for sub in taxes if sub['title'] == "KKDF" and sub['id'] == 1), 0)

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
                total_expense += expense

            base_investment = initial_investment - total_expense

            for credit in credits:
                cash_flows.append(credit)
            irr = get_irr(float(base_investment), cash_flows)

            for credit in credits:
                #current_amount = initial_investment
                _interest = calculate_interest(current_amount, irr)
                _tax = calculate_tax(_interest, tax_bsmv, tax_kkdf)
                _principal_amount = calculate_prn(credit, _interest, _tax)
                _remaining_principal_amount = calculate_rm_prn(current_amount, _principal_amount)

                credit_table = CreditTable(
                    credit_amount=credit,
                    interest=_interest,
                    tax=_tax,
                    principal_amount=_principal_amount,
                    remaining_principal_amount=_remaining_principal_amount
                    )
                credit_table_list.append(credit_table)
                current_amount = _remaining_principal_amount

            all_expenses_title = "Peşin Ödenen Masraflar (Vergiler Dahil)"
            table = credit_table_list
            data_irr = {"irr": irr, "table": serializers.serialize('json', table)}
            response = Response(data=data_irr, status=status.HTTP_200_OK)

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)