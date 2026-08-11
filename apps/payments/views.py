from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from apps.businesses.mixins import TenantMixin
from apps.credit.services import record_payment
from apps.businesses.models import BusinessMember

@login_required
def payment_list_view(request):
    membership = BusinessMember.objects.filter(user=request.user).first()
    if not membership:
        return render(request, 'no_business.html')
    
    payments = Payment.objects.filter(business=membership.business)
    return render(request, 'payments/payment_list.html', {'payments': payments})

class PaymentViewSet(TenantMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ['customer', 'method', 'payment_date']

    def create(self, request, *args, **kwargs):
        business = self.get_business()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment = record_payment(
            business=business,
            customer=serializer.validated_data['customer'],
            amount=serializer.validated_data['amount'],
            payment_date=serializer.validated_data['payment_date'],
            method=serializer.validated_data['method'],
            reference_number=serializer.validated_data.get('reference_number', ''),
            notes=serializer.validated_data.get('notes', ''),
            user=request.user
        )
        
        output_serializer = self.get_serializer(payment)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
