from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    OWNER = 'OWNER', _('Owner')
    STAFF = 'STAFF', _('Staff')
    ACCOUNTANT = 'ACCOUNTANT', _('Accountant')
    CUSTOMER = 'CUSTOMER', _('Customer')
    ADMIN = 'ADMIN', _('Admin')
