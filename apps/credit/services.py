from django.db import transaction
from django.utils import timezone
from apps.credit.models import CreditAccount, CreditSale
from apps.payments.models import Payment, PaymentAllocation
from apps.audit.models import CreditEvent
from decimal import Decimal
from django.core.exceptions import ValidationError

@transaction.atomic
def record_credit_sale(business, customer, amount, sale_date, due_date, description="", reference_number="", user=None):
    sale = CreditSale.objects.create(
        business=business,
        customer=customer,
        amount=amount,
        sale_date=sale_date,
        due_date=due_date,
        description=description,
        reference_number=reference_number
    )
    
    # Update Credit Account
    account, created = CreditAccount.objects.get_or_create(customer=customer)
    account.current_balance += amount
    account.total_credit_granted += amount
    account.save()
    
    # Record Event
    CreditEvent.objects.create(
        business=business,
        event_type='CREDIT_CREATED',
        description=f"Credit sale of {amount} created for {customer.name}",
        user=user,
        content_object=sale
    )

    # Update Intelligence Scores
    from apps.intelligence.services.collection_priority import calculate_collection_priority
    calculate_collection_priority(customer)
    
    return sale

@transaction.atomic
def record_payment(business, customer, amount, payment_date, method, reference_number="", notes="", user=None):
    # Update Credit Account
    account, created = CreditAccount.objects.get_or_create(customer=customer)
    
    if amount > account.current_balance:
        raise ValidationError(f"Payment amount {amount} exceeds current outstanding balance {account.current_balance}")

    payment = Payment.objects.create(
        business=business,
        customer=customer,
        amount=amount,
        payment_date=payment_date,
        method=method,
        reference_number=reference_number,
        notes=notes
    )
    
    account.current_balance -= amount
    account.total_paid += amount
    account.save()
    
    # Allocate payment to pending sales (FIFO)
    remaining_to_allocate = amount
    pending_sales = CreditSale.objects.filter(
        customer=customer,
        status__in=['PENDING', 'PARTIALLY_PAID', 'OVERDUE']
    ).order_by('sale_date', 'id')
    
    for sale in pending_sales:
        if remaining_to_allocate <= 0:
            break
            
        unpaid_amount = sale.amount - sale.paid_amount
        allocation_amount = min(remaining_to_allocate, unpaid_amount)
        
        if allocation_amount > 0:
            PaymentAllocation.objects.create(
                payment=payment,
                credit_sale=sale,
                allocated_amount=allocation_amount
            )
            sale.paid_amount += allocation_amount
            if sale.paid_amount >= sale.amount:
                sale.status = 'PAID'
            else:
                sale.status = 'PARTIALLY_PAID'
            sale.save()
            
            remaining_to_allocate -= allocation_amount
            
            # Record Allocation Event
            CreditEvent.objects.create(
                business=business,
                event_type='PAYMENT_ALLOCATED',
                description=f"Allocated {allocation_amount} to sale {sale.id}",
                user=user,
                content_object=payment
            )

    # Record Payment Event
    CreditEvent.objects.create(
        business=business,
        event_type='PAYMENT_RECEIVED',
        description=f"Payment of {amount} received from {customer.name}",
        user=user,
        content_object=payment
    )
    
    # Update Intelligence Scores
    from apps.intelligence.services.reliability import calculate_reliability_score
    from apps.intelligence.services.collection_priority import calculate_collection_priority
    calculate_reliability_score(customer)
    calculate_collection_priority(customer)
    
    return payment
