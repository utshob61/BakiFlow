from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Business(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_businesses'
    )

    class Meta:
        verbose_name_plural = _("Businesses")

    def __str__(self):
        return self.name

from apps.accounts.roles import UserRole

class BusinessMember(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STAFF
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('business', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.business.name} ({self.role})"
