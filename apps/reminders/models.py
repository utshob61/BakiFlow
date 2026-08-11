from django.db import models
from apps.customers.models import Customer
from apps.businesses.models import Business

class Reminder(models.Model):
    class Type(models.TextChoices):
        DUE_DATE = 'DUE_DATE', 'Due Date'
        OVERDUE = 'OVERDUE', 'Overdue'
        MANUAL = 'MANUAL', 'Manual'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SENT = 'SENT', 'Sent'
        FAILED = 'FAILED', 'Failed'
        DISMISSED = 'DISMISSED', 'Dismissed'

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='reminders'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='reminders'
    )
    reminder_type = models.CharField(max_length=20, choices=Type.choices)
    scheduled_for = models.DateTimeField()
    message_template = models.TextField()
    generated_message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Reminder for {self.customer.name} on {self.scheduled_for}"
