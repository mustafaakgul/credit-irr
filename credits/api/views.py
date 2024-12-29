from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView

from credits.api.serializers import IRRCreditCreateSerializer
from credits.models import IRRTable
from credits.utils.irr_func import get_irr


class IRRTableGenericAPIView(CreateAPIView):
    queryset = IRRTable.objects.all()
    serializer_class = IRRCreditCreateSerializer
    permission_classes = [AllowAny]

class IRRTableAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = IRRCreditCreateSerializer(data=request.data)
        if serializer.is_valid():
            cash_flows = []
            initial_investment = serializer.data['initial']
            credits = serializer.data['credits']

            for credit in credits:
                cash_flows.append(credit)

            print("IRR Table Values: ", initial_investment, credits)
            irr = get_irr(float(initial_investment), cash_flows)
            print(irr)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)