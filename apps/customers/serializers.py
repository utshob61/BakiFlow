from rest_framework import serializers
from apps.customers.models import Customer
from apps.intelligence.models import ReliabilityScore, CollectionPriority

class ReliabilityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReliabilityScore
        fields = ('score', 'on_time_payment_component', 'consistency_component', 'delay_component', 'recent_behavior_component', 'trend_component')

class CollectionPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionPriority
        fields = ('score', 'level', 'factors')

class CustomerSerializer(serializers.ModelSerializer):
    reliability_score = ReliabilityScoreSerializer(read_only=True)
    collection_priority = CollectionPrioritySerializer(read_only=True)
    outstanding_balance = serializers.DecimalField(
        source='credit_account.current_balance',
        max_digits=15,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('business',)
