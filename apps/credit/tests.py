from django.test import TestCase
from django.utils import timezone
from apps.accounts.models import User
from apps.businesses.models import Business, BusinessMember
from apps.customers.models import Customer
from apps.credit.models import CreditAccount, CreditSale
from apps.credit.services import record_credit_sale, record_payment
from decimal import Decimal
from django.core.exceptions import ValidationError

class CreditServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.business = Business.objects.create(name='Test Business', slug='test-business', owner=self.user)
        BusinessMember.objects.create(business=self.business, user=self.user, role='OWNER')
        self.customer = Customer.objects.create(business=self.business, name='Test Customer', phone='01700000000')

    def test_record_credit_sale(self):
        amount = Decimal('1000.00')
        sale_date = timezone.now().date()
        due_date = sale_date + timezone.timedelta(days=7)
        
        sale = record_credit_sale(
            business=self.business,
            customer=self.customer,
            amount=amount,
            sale_date=sale_date,
            due_date=due_date,
            user=self.user
        )
        
        self.assertEqual(sale.amount, amount)
        account = CreditAccount.objects.get(customer=self.customer)
        self.assertEqual(account.current_balance, amount)

    def test_record_payment_and_allocation(self):
        # Create a sale
        record_credit_sale(
            business=self.business,
            customer=self.customer,
            amount=Decimal('1000.00'),
            sale_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=7),
            user=self.user
        )
        
        # Record partial payment
        payment_amount = Decimal('400.00')
        record_payment(
            business=self.business,
            customer=self.customer,
            amount=payment_amount,
            payment_date=timezone.now(),
            method='CASH',
            user=self.user
        )
        
        sale = CreditSale.objects.get(customer=self.customer)
        self.assertEqual(sale.paid_amount, payment_amount)
        self.assertEqual(sale.status, 'PARTIALLY_PAID')
        
        account = CreditAccount.objects.get(customer=self.customer)
        self.assertEqual(account.current_balance, Decimal('600.00'))

    def test_overpayment_prevention(self):
        # Create a sale of 1000
        record_credit_sale(
            business=self.business,
            customer=self.customer,
            amount=Decimal('1000.00'),
            sale_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=7),
            user=self.user
        )
        
        # Try to pay 1500
        with self.assertRaises(ValidationError):
            record_payment(
                business=self.business,
                customer=self.customer,
                amount=Decimal('1500.00'),
                payment_date=timezone.now(),
                method='CASH',
                user=self.user
            )
