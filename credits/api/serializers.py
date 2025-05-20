from rest_framework.serializers import ModelSerializer

from credits.models import IRRTable


class IRRCreditCreateSerializer(ModelSerializer):
    class Meta:
        model = IRRTable
        fields = ('initial', 'credits', 'credit_type', 'consumer_credit_type', 'expenses', 'block', 'block_amount', 'taxes')

    def validate_initial(self, value):
        if value is None:
            raise serializers.ValidationError("Başlangıç değeri boş bırakılamaz.")
        if value <= 0:
            raise serializers.ValidationError("Başlangıç değeri 0'dan büyük olmalıdır.")
        return value
