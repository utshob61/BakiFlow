from django.db import models
from apps.customers.models import Customer
from decimal import Decimal

class ReliabilityScore(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='reliability_score'
    )
    score = models.IntegerField(default=0) # 0-100
    on_time_payment_component = models.IntegerField(default=0)
    consistency_component = models.IntegerField(default=0)
    delay_component = models.IntegerField(default=0)
    recent_behavior_component = models.IntegerField(default=0)
    trend_component = models.IntegerField(default=0)
    calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - {self.score}/100"

class CollectionPriority(models.Model):
    class PriorityLevel(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='collection_priority'
    )
    score = models.IntegerField(default=0) # 0-100
    level = models.CharField(
        max_length=20,
        choices=PriorityLevel.choices,
        default=PriorityLevel.LOW
    )
    factors = models.JSONField(default=dict)
    calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - {self.level} ({self.score})"

class FinancialHealth(models.Model):
    business = models.OneToOneField(
        'businesses.Business',
        on_delete=models.CASCADE,
        related_name='financial_health'
    )
    score = models.IntegerField(default=0) # 0-100
    factors = models.JSONField(default=dict)
    calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business.name} - {self.score}/100"
