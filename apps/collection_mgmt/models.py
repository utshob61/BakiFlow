from django.db import models
from apps.customers.models import Customer
from apps.businesses.models import Business

class CollectionTask(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        POSTPONED = 'POSTPONED', 'Postponed'

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='collection_tasks'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='collection_tasks'
    )
    due_date = models.DateField()
    priority_score = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_collection_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task for {self.customer.name} - {self.due_date}"

class FollowUpAttempt(models.Model):
    task = models.ForeignKey(
        CollectionTask,
        on_delete=models.CASCADE,
        related_name='follow_ups'
    )
    contacted_at = models.DateTimeField(auto_now_add=True)
    contact_method = models.CharField(max_length=50) # e.g., Phone, SMS, In-Person
    outcome = models.TextField()
    next_follow_up_date = models.DateField(null=True, blank=True)
    recorded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"Follow up for {self.task.customer.name} at {self.contacted_at}"
