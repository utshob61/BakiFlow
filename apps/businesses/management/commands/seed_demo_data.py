from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User
from apps.businesses.models import Business, BusinessMember
from apps.customers.models import Customer
from apps.credit.services import record_credit_sale, record_payment
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Seed demo data for BakiFlow'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding demo data...')
        
        # 1. Create Owner
        owner, _ = User.objects.get_or_create(
            username='owner',
            defaults={'email': 'owner@example.com', 'role': 'OWNER'}
        )
        owner.set_password('password123')
        owner.save()
            
        # 2. Create Business
        business, _ = Business.objects.get_or_create(
            slug='dhaka-traders',
            defaults={'name': 'Dhaka Traders', 'owner': owner, 'phone': '01711111111'}
        )
        
        BusinessMember.objects.get_or_create(
            business=business, user=owner, defaults={'role': 'OWNER'}
        )

        # 3. Create Customer User
        customer_user, _ = User.objects.get_or_create(
            username='rahim',
            defaults={'email': 'rahim@example.com', 'role': 'CUSTOMER'}
        )
        customer_user.set_password('password123')
        customer_user.save()
        
        # Clear existing link for this user to avoid unique constraint error
        Customer.objects.filter(user=customer_user).update(user=None)

        # 4. Create Customers and Transactions
        customer_names = ['Abul', 'Kabul', 'Rahim', 'Karim', 'Sakib', 'Tamim', 'Mushfiq', 'Mahmudullah']
        for name in customer_names:
            customer, created = Customer.objects.get_or_create(
                business=business, 
                name=name,
                defaults={'phone': f"018{random.randint(10000000, 99999999)}"}
            )
            
            if name == 'Rahim':
                customer.user = customer_user
                customer.save()
            
            if created or not customer.credit_sales.exists():
                for _ in range(random.randint(2, 5)):
                    record_credit_sale(
                        business=business,
                        customer=customer,
                        amount=Decimal(random.randint(5000, 25000)),
                        sale_date=timezone.now().date() - timezone.timedelta(days=random.randint(10, 60)),
                        due_date=timezone.now().date() + timezone.timedelta(days=15),
                        description=f"Standard supply for {name}",
                        user=owner
                    )
                    
                for _ in range(random.randint(1, 3)):
                    record_payment(
                        business=business,
                        customer=customer,
                        amount=Decimal(random.randint(2000, 8000)),
                        payment_date=timezone.now() - timezone.timedelta(days=random.randint(1, 5)),
                        method='CASH',
                        user=owner
                    )

        self.stdout.write(self.style.SUCCESS('Successfully seeded demo data'))
