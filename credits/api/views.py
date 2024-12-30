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

            irr = get_irr(float(initial_investment), cash_flows)
            data_irr = {"irr": irr}
            response = Response(data=data_irr, status=status.HTTP_400_BAD_REQUEST)

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)