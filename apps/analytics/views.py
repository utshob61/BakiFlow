from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.businesses.models import BusinessMember
from apps.customers.models import Customer
from apps.credit.models import CreditSale
from apps.payments.models import Payment
from apps.intelligence.models import CollectionPriority
from django.db.models import Sum, Q
from decimal import Decimal
from django.utils import timezone

@login_required
def dashboard(request):
    # Check if user is a Customer
    if request.user.role == 'CUSTOMER':
        customer = getattr(request.user, 'customer_profile', None)
        if not customer:
            return render(request, 'no_customer_profile.html')
        
        account = getattr(customer, 'credit_account', None)
        sales = CreditSale.objects.filter(customer=customer).order_by('-sale_date')[:5]
        payments = Payment.objects.filter(customer=customer).order_by('-payment_date')[:5]
        
        context = {
            'customer': customer,
            'account': account,
            'sales': sales,
            'payments': payments,
            'is_customer': True
        }
        return render(request, 'customers/dashboard.html', context)

    # Business Owner/Staff View
    membership = BusinessMember.objects.filter(user=request.user).select_related('business').first()
    
    if not membership:
        if request.user.is_superuser:
            from apps.businesses.models import Business
            business = Business.objects.first()
            if not business:
                return render(request, 'no_business.html', {'is_admin': True})
        else:
            return render(request, 'no_business.html')
    else:
        business = membership.business

    today = timezone.now().date()
    
    # Receivables Aggregation
    receivables_agg = CreditSale.objects.filter(
        business=business,
        status__in=['PENDING', 'PARTIALLY_PAID', 'OVERDUE']
    ).aggregate(
        total_amount=Sum('amount'),
        total_paid=Sum('paid_amount')
    )
    total_receivables = (receivables_agg['total_amount'] or Decimal('0.00')) - (receivables_agg['total_paid'] or Decimal('0.00'))
    
    overdue_agg = CreditSale.objects.filter(
        business=business,
        status__in=['PENDING', 'PARTIALLY_PAID', 'OVERDUE'],
        due_date__lt=today
    ).aggregate(
        total_amount=Sum('amount'),
        total_paid=Sum('paid_amount')
    )
    overdue_receivables = (overdue_agg['total_amount'] or Decimal('0.00')) - (overdue_agg['total_paid'] or Decimal('0.00'))
    
    # Monthly Collections
    collected_this_month = Payment.objects.filter(
        business=business,
        payment_date__month=today.month,
        payment_date__year=today.year
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    # Real Collection Priorities
    priorities = CollectionPriority.objects.filter(
        customer__business=business,
        score__gt=0
    ).select_related('customer', 'customer__credit_account').order_by('-score')[:5]
    
    context = {
        'business': business,
        'total_receivables': total_receivables,
        'overdue_receivables': overdue_receivables,
        'collected_this_month': collected_this_month,
        'priorities': priorities,
    }
    return render(request, 'dashboard.html', context)
