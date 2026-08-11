from django.test import TestCase
from django.utils import timezone
from apps.accounts.models import User
from apps.businesses.models import Business
from apps.customers.models import Customer
from apps.credit.services import record_credit_sale, record_payment
from apps.intelligence.services.reliability import calculate_reliability_score
from apps.intelligence.services.collection_priority import calculate_collection_priority
from decimal import Decimal

class IntelligenceServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.business = Business.objects.create(name='Test Business', slug='test-business', owner=self.user)
        self.customer = Customer.objects.create(business=self.business, name='Test Customer', phone='01700000000')

    def test_reliability_score_calculation(self):
        # Create an on-time paid sale
        sale_date = timezone.now().date() - timezone.timedelta(days=20)
        due_date = sale_date + timezone.timedelta(days=10) # Overdue by 10 days if not paid
        
        record_credit_sale(
            business=self.business,
            customer=self.customer,
            amount=Decimal('1000.00'),
            sale_date=sale_date,
            due_date=due_date,
            user=self.user
        )
        
        # Pay it on time (payment date < due date)
        record_payment(
            business=self.business,
            customer=self.customer,
            amount=Decimal('1000.00'),
            payment_date=timezone.make_aware(timezone.datetime.combine(sale_date + timezone.timedelta(days=2), timezone.datetime.min.time())),
            method='CASH',
            user=self.user
        )
        
        score_obj = calculate_reliability_score(self.customer)
        self.assertIsNotNone(score_obj)
        # On-time payments should be 100%, so 30/30 pts for that component
        self.assertEqual(score_obj.on_time_payment_component, 30)

    def test_collection_priority_calculation(self):
        # Create an overdue sale
        sale_date = timezone.now().date() - timezone.timedelta(days=40)
        due_date = sale_date + timezone.timedelta(days=5) # Overdue by 35 days
        
        record_credit_sale(
            business=self.business,
            customer=self.customer,
            amount=Decimal('50000.00'),
            sale_date=sale_date,
            due_date=due_date,
            user=self.user
        )
        
        priority_obj = calculate_collection_priority(self.customer)
        self.assertIsNotNone(priority_obj)
        # Should be CRITICAL or HIGH because it's 35 days overdue
        self.assertIn(priority_obj.level, ['HIGH', 'CRITICAL'])
