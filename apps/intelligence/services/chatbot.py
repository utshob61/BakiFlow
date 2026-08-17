from decimal import Decimal
from apps.credit.models import CreditSale
from apps.customers.models import Customer
from apps.payments.models import Payment
from django.db.models import Sum

def process_bot_query(business, query):
    """
    Deterministic AI Assistant for BakiFlow.
    Robust handling for common SME queries and misspellings.
    """
    q = query.lower().strip()
    
    # 1. Handle Greetings
    greetings = ["hi", "hello", "hey", "assalamu alaikum", "aoa", "slm"]
    for greet in greetings:
        if greet in q:
            return "I'm your BakiFlow assistant. I can tell you about your 'total baki', 'top debtors', or 'monthly collections'. What would you like to know?"

    # 2. Top Debtors (Catches 'top debotors', 'who owes most', etc.)
    debtor_triggers = ["debtor", "debotor", "owe", "most", "highest", "top"]
    is_debtor_query = False
    for trigger in debtor_triggers:
        if trigger in q:
            is_debtor_query = True
            break
            
    if is_debtor_query:
        top_customer = Customer.objects.filter(business=business).order_by('-credit_account__current_balance').first()
        if top_customer and top_customer.credit_account.current_balance > 0:
            return f"{top_customer.name} owes you the most right now, with an outstanding balance of ৳{top_customer.credit_account.current_balance:,.2f}."
        return "You have no outstanding debtors! Your collections are fully up to date. 🎉"

    # 3. Total Baki / Receivables
    baki_triggers = ["total", "summary", "overall", "baki", "outstanding", "balance"]
    # Check if user is asking for a summary/total
    if "total" in q or "baki" in q or "outstanding" in q:
        agg = CreditSale.objects.filter(
            business=business, 
            status__in=['PENDING', 'PARTIALLY_PAID', 'OVERDUE']
        ).aggregate(
            total=Sum('amount'), paid=Sum('paid_amount')
        )
        total_val = (agg['total'] or Decimal('0.00')) - (agg['paid'] or Decimal('0.00'))
        return f"Your business has a total of ৳{total_val:,.2f} in outstanding Baki across all customers."

    # 4. Monthly Collection Progress
    if "collect" in q or "received" in q or "cash" in q or "payment" in q:
        from django.utils import timezone
        today = timezone.now().date()
        total_coll = Payment.objects.filter(
            business=business, 
            payment_date__month=today.month, 
            payment_date__year=today.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        return f"You have collected a total of ৳{total_coll:,.2f} in cash so far this month."

    # 5. Polite Fallbacks
    if "thanks" in q or "thank you" in q or "ok" in q:
        return "Happy to help! Let me know if you need more insights. 🚀"

    return "I'm not quite sure about that. I can currently help with total Baki, top debtors, and monthly collection updates. Try asking: 'Who owes me the most?'"
