from decimal import Decimal
from django.utils import timezone
from apps.intelligence.models import ReliabilityScore
from apps.credit.models import CreditSale
from apps.payments.models import PaymentAllocation

def calculate_reliability_score(customer):
    """
    Calculates the Payment Reliability Score for a customer.
    Score range: 0-100
    """
    sales = CreditSale.objects.filter(customer=customer)
    if not sales.exists():
        return None

    # 1. On-time payments (30 pts)
    # % of sales where paid_amount >= amount before due_date
    total_sales = sales.count()
    on_time_sales = 0
    for sale in sales:
        allocations = PaymentAllocation.objects.filter(credit_sale=sale)
        if not allocations.exists() and sale.due_date < timezone.now().date():
            continue
        
        fully_paid_on_time = False
        cumulative_paid = Decimal('0.00')
        for alloc in allocations.select_related('payment').order_by('payment__payment_date'):
            cumulative_paid += alloc.allocated_amount
            if cumulative_paid >= sale.amount:
                if alloc.payment.payment_date.date() <= sale.due_date:
                    fully_paid_on_time = True
                break
        if fully_paid_on_time:
            on_time_sales += 1
    
    on_time_pts = int((on_time_sales / total_sales) * 30)

    # 2. Payment consistency (20 pts)
    # Frequency of payments vs expected (simplified for now)
    consistency_pts = 10 # Placeholder

    # 3. Average delay (20 pts)
    # Average days past due for all payments
    delay_pts = 10 # Placeholder

    # 4. Recent behavior (15 pts)
    # Last 3 months behavior
    recent_pts = 10 # Placeholder

    # 5. Outstanding trend (15 pts)
    # Is balance growing or shrinking
    trend_pts = 5 # Placeholder

    total_score = on_time_pts + consistency_pts + delay_pts + recent_pts + trend_pts
    
    score_obj, created = ReliabilityScore.objects.update_or_create(
        customer=customer,
        defaults={
            'score': total_score,
            'on_time_payment_component': on_time_pts,
            'consistency_component': consistency_pts,
            'delay_component': delay_pts,
            'recent_behavior_component': recent_pts,
            'trend_component': trend_pts,
        }
    )
    return score_obj
