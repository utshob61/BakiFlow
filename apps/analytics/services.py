from django.utils import timezone
from django.db.models import Sum
from apps.credit.models import CreditSale
from decimal import Decimal

def get_aging_report(business):
    today = timezone.now().date()
    sales = CreditSale.objects.filter(
        business=business,
        status__in=['PENDING', 'PARTIALLY_PAID', 'OVERDUE']
    )
    
    buckets = {
        'current': Decimal('0.00'),
        '1-7': Decimal('0.00'),
        '8-30': Decimal('0.00'),
        '31-60': Decimal('0.00'),
        '61-90': Decimal('0.00'),
        '90+': Decimal('0.00'),
    }
    
    for sale in sales:
        remaining = sale.amount - sale.paid_amount
        if remaining <= 0: continue
        
        if sale.due_date >= today:
            buckets['current'] += remaining
        else:
            days_overdue = (today - sale.due_date).days
            if days_overdue <= 7: buckets['1-7'] += remaining
            elif days_overdue <= 30: buckets['8-30'] += remaining
            elif days_overdue <= 60: buckets['31-60'] += remaining
            elif days_overdue <= 90: buckets['61-90'] += remaining
            else: buckets['90+'] += remaining
            
    return buckets
