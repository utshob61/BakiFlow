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
        
        # Create Owner
        owner, created = User.objects.get_or_create(
            username='owner',
            email='owner@example.com',
            defaults={'role': 'OWNER'}
        )
        if created:
            owner.set_password('password123')
            owner.save()
            
        # Create Business
        business, created = Business.objects.get_or_create(
            slug='dhaka-traders',
            defaults={
                'name': 'Dhaka Traders',
                'owner': owner,
                'phone': '01711111111'
            }
        )
        
        BusinessMember.objects.get_or_create(
            business=business,
            user=owner,
            defaults={'role': 'OWNER'}
        )
        
        # Create Customers
        customer_names = ['Abul', 'Kabul', 'Rahim', 'Karim', 'Sakib', 'Tamim', 'Mushfiq', 'Mahmudullah']
        for name in customer_names:
            customer, created = Customer.objects.get_or_create(
                business=business,
                phone=f"018{random.randint(10000000, 99999999)}",
                defaults={'name': name}
            )
            
            # Create some credit sales
            for _ in range(random.randint(1, 5)):
                amount = Decimal(random.randint(1000, 20000))
                sale_date = timezone.now().date() - timezone.timedelta(days=random.randint(1, 60))
                due_date = sale_date + timezone.timedelta(days=15)
                
                record_credit_sale(
                    business=business,
                    customer=customer,
                    amount=amount,
                    sale_date=sale_date,
                    due_date=due_date,
                    description=f"Sale of products for {name}",
                    user=owner
                )
                
            # Create some partial payments
            for _ in range(random.randint(0, 3)):
                amount = Decimal(random.randint(500, 5000))
                payment_date = timezone.now()
                record_payment(
                    business=business,
                    customer=customer,
                    amount=amount,
                    payment_date=payment_date,
                    method='CASH',
                    user=owner
                )

        # Create a Customer User for testing
        customer_user, created = User.objects.get_or_create(
            username='rahim',
            email='rahim@example.com',
            defaults={'role': 'CUSTOMER'}
        )
        if created:
            customer_user.set_password('password123')
            customer_user.save()
            
        # Link Rahim customer to this user
        rahim_customer = Customer.objects.filter(name='Rahim').first()
        if rahim_customer:
            rahim_customer.user = customer_user
            rahim_customer.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded demo data'))
