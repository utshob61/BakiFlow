from django.test import TestCase
from apps.accounts.models import User
from apps.businesses.models import Business, BusinessMember
from apps.customers.models import Customer
from rest_framework.test import APIClient

class TenantIsolationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='u1@example.com', password='password')
        self.user2 = User.objects.create_user(username='user2', email='u2@example.com', password='password')
        
        self.business1 = Business.objects.create(name='Business 1', slug='b1', owner=self.user1)
        BusinessMember.objects.create(business=self.business1, user=self.user1, role='OWNER')
        
        self.business2 = Business.objects.create(name='Business 2', slug='b2', owner=self.user2)
        BusinessMember.objects.create(business=self.business2, user=self.user2, role='OWNER')
        
        Customer.objects.create(business=self.business1, name='Customer B1', phone='111')
        Customer.objects.create(business=self.business2, name='Customer B2', phone='222')
        
        self.client = APIClient()

    def test_tenant_isolation_customers(self):
        # Login as user 1
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/v1/customers/')
        
        self.assertEqual(response.status_code, 200)
        # Should only see 1 customer (from business 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Customer B1')
        
        # Login as user 2
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/v1/customers/')
        
        self.assertEqual(response.status_code, 200)
        # Should only see 1 customer (from business 2)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Customer B2')
