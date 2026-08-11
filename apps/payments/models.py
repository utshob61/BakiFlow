from django.db import models
from django.conf import settings
from apps.customers.models import Customer
from apps.credit.models import CreditSale
from decimal import Decimal

class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = 'CASH', 'Cash'
        BKASH = 'BKASH', 'bKash'
        NAGAD = 'NAGAD', 'Nagad'
        BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'
        CARD = 'CARD', 'Card'
        OTHER = 'OTHER', 'Other'

    business = models.ForeignKey(
        'businesses.Business',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateTimeField()
    method = models.CharField(
        max_length=20,
        choices=Method.choices,
        default=Method.CASH
    )
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_date', '-created_at']

    def __str__(self):
        return f"Payment {self.id} - {self.customer.name} - {self.amount}"

class PaymentAllocation(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='allocations'
    )
    credit_sale = models.ForeignKey(
        CreditSale,
        on_delete=models.CASCADE,
        related_name='allocations'
    )
    allocated_amount = models.DecimalField(max_digits=15, decimal_places=2)
    allocated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-allocated_at']

    def __str__(self):
        return f"Allocation {self.id} - {self.payment.id} to Sale {self.credit_sale.id}"
