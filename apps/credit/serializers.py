from rest_framework import serializers
from apps.credit.models import CreditSale, CreditAccount

class CreditSaleSerializer(serializers.ModelSerializer):
    remaining_balance = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = CreditSale
        fields = '__all__'
        read_only_fields = ('business', 'paid_amount', 'status')

class CreditAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditAccount
        fields = '__all__'
