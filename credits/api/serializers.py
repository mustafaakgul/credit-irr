from rest_framework.serializers import ModelSerializer

from credits.models import IRRTable


class IRRCreditCreateSerializer(ModelSerializer):
    class Meta:
        model = IRRTable
        fields = ('initial', 'credits', 'credit_type', 'consumer_credit_type', 'expenses', 'block', 'block_amount', 'taxes')

    # def validate(self, attrs):
    #     if(attrs["parent"]):
    #         if attrs["parent"].post != attrs["post"]:
    #             raise serializers.ValidationError("Hata oluştu. Lütfen tekrar deneyiniz.")
    #     return attrs
