from django.utils import timezone
from apps.intelligence.models import CollectionPriority
from apps.credit.models import CreditAccount, CreditSale

def calculate_collection_priority(customer):
    """
    Calculates the Collection Priority Score for a customer.
    Score range: 0-100
    """
    account = CreditAccount.objects.get(customer=customer)
    
    overdue_sales = CreditSale.objects.filter(
        customer=customer,
        status__in=['PENDING', 'PARTIALLY_PAID', 'OVERDUE'],
        due_date__lt=timezone.now().date()
    )
    
    if not overdue_sales.exists() and account.current_balance <= 0:
        return None

    # Factors:
    # 1. Overdue amount (relative to total balance)
    # 2. Days overdue (max days)
    # 3. Reliability score (inverse)
    
    overdue_amount = sum(sale.remaining_balance for sale in overdue_sales)
    max_days_overdue = 0
    if overdue_sales.exists():
        oldest_sale = overdue_sales.order_by('due_date').first()
        max_days_overdue = (timezone.now().date() - oldest_sale.due_date).days

    # Scoring logic (simplified)
    score = 0
    if overdue_amount > 0:
        score += 30 # Base for having overdue
        if overdue_amount > 10000: score += 10
        if overdue_amount > 50000: score += 10

    if max_days_overdue > 30: score += 20
    elif max_days_overdue > 7: score += 10
    
    # Priority Level
    level = CollectionPriority.PriorityLevel.LOW
    if score >= 80: level = CollectionPriority.PriorityLevel.CRITICAL
    elif score >= 60: level = CollectionPriority.PriorityLevel.HIGH
    elif score >= 40: level = CollectionPriority.PriorityLevel.MEDIUM

    priority_obj, created = CollectionPriority.objects.update_or_create(
        customer=customer,
        defaults={
            'score': min(score, 100),
            'level': level,
            'factors': {
                'overdue_amount': float(overdue_amount),
                'max_days_overdue': max_days_overdue,
            }
        }
    )
    return priority_obj
