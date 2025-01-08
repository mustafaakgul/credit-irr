from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core import serializers

from rest_framework.views import APIView

from credits.api.serializers import IRRCreditCreateSerializer
from credits.models import IRRTable, CreditTable
from credits.utils.irr_func import get_irr, calculate_interest, calculate_tax, calculate_prn, calculate_rm_prn


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
            cash_flows = []
            credit_table_list = []
            initial_investment = serializer.data['initial']
            current_amount = initial_investment
            credits = serializer.data['credits']
            credit_type = serializer.data['credit_type']
            consumer_credit_type = serializer.data['consumer_credit_type']

            if (initial_investment < 0):
                return Response({"Error": "Kredi Tutarı eksi bir değer olamaz."}, status=status.HTTP_400_BAD_REQUEST)

            for credit in credits:
                cash_flows.append(credit)
            irr = get_irr(float(initial_investment), cash_flows)

            for credit in credits:
                #current_amount = initial_investment
                _interest = calculate_interest(current_amount, irr)
                _tax = calculate_tax(_interest)
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

            table = credit_table_list
            data_irr = {"irr": irr, "table": serializers.serialize('json', table)}
            response = Response(data=data_irr, status=status.HTTP_200_OK)

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)