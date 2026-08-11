import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import action
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer
from apps.businesses.mixins import TenantMixin
from apps.businesses.models import BusinessMember

@login_required
def customer_list_view(request):
    membership = BusinessMember.objects.filter(user=request.user).first()
    if not membership:
        return render(request, 'no_business.html')
    
    customers = Customer.objects.filter(business=membership.business)
    return render(request, 'customers/customer_list.html', {'customers': customers})

class CustomerViewSet(TenantMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ['name', 'phone']
    filterset_fields = ['status']

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        business = self.get_business()
        customers = self.get_queryset()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{business.slug}_customers.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Phone', 'Email', 'Status', 'Outstanding Balance'])
        
        for customer in customers:
            balance = getattr(customer.credit_account, 'current_balance', 0)
            writer.writerow([customer.name, customer.phone, customer.email, customer.status, balance])
            
        return response
