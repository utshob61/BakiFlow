from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CreditEvent(models.Model):
    class EventType(models.TextChoices):
        CREDIT_CREATED = 'CREDIT_CREATED', 'Credit Created'
        PAYMENT_RECEIVED = 'PAYMENT_RECEIVED', 'Payment Received'
        PAYMENT_ALLOCATED = 'PAYMENT_ALLOCATED', 'Payment Allocated'
        CREDIT_ADJUSTED = 'CREDIT_ADJUSTED', 'Credit Adjusted'
        CREDIT_WRITTEN_OFF = 'CREDIT_WRITTEN_OFF', 'Credit Written Off'
        DUE_DATE_CHANGED = 'DUE_DATE_CHANGED', 'Due Date Changed'
        CUSTOMER_CREATED = 'CUSTOMER_CREATED', 'Customer Created'

    business = models.ForeignKey(
        'businesses.Business',
        on_delete=models.CASCADE,
        related_name='credit_events'
    )
    event_type = models.CharField(max_length=50, choices=EventType.choices)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Generic relation to the object involved in the event
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.event_type} - {self.timestamp}"

class AuditLog(models.Model):
    business = models.ForeignKey(
        'businesses.Business',
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"
