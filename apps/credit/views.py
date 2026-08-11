from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.credit.models import CreditSale
from apps.credit.serializers import CreditSaleSerializer
from apps.businesses.mixins import TenantMixin
from apps.credit.services import record_credit_sale
from apps.businesses.models import BusinessMember

@login_required
def credit_sale_list_view(request):
    membership = BusinessMember.objects.filter(user=request.user).first()
    if not membership:
        return render(request, 'no_business.html')
    
    sales = CreditSale.objects.filter(business=membership.business)
    return render(request, 'credit/credit_sale_list.html', {'sales': sales})

class CreditSaleViewSet(TenantMixin, viewsets.ModelViewSet):
    queryset = CreditSale.objects.all()
    serializer_class = CreditSaleSerializer
    filterset_fields = ['customer', 'status', 'sale_date', 'due_date']

    def create(self, request, *args, **kwargs):
        business = self.get_business()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        sale = record_credit_sale(
            business=business,
            customer=serializer.validated_data['customer'],
            amount=serializer.validated_data['amount'],
            sale_date=serializer.validated_data['sale_date'],
            due_date=serializer.validated_data['due_date'],
            description=serializer.validated_data.get('description', ''),
            reference_number=serializer.validated_data.get('reference_number', ''),
            user=request.user
        )
        
        output_serializer = self.get_serializer(sale)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
