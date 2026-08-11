from django.utils import timezone
from apps.reminders.models import Reminder

def generate_reminder_message(customer, amount_due, language='bn'):
    templates = {
        'bn': "আসসালামু আলাইকুম {name} ভাই, আপনার কাছে আমাদের ৳{amount} টাকা বাকি আছে। সুবিধামতো পরিশোধ করলে কৃতজ্ঞ থাকব।",
        'en': "Assalamu Alaikum {name}, you have an outstanding balance of ৳{amount} with us. We would appreciate it if you could settle it at your convenience.",
        'banglish': "Assalamu Alaikum {name} bhai, apnar kache amader ৳{amount} taka baki ache. Shuvidhamoto porishodh korle kritoggo thakbo."
    }
    
    template = templates.get(language, templates['bn'])
    return template.format(name=customer.name, amount=f"{amount_due:,.2f}")

def create_due_date_reminder(sale):
    message = generate_reminder_message(sale.customer, sale.remaining_balance)
    return Reminder.objects.create(
        business=sale.business,
        customer=sale.customer,
        reminder_type='DUE_DATE',
        scheduled_for=timezone.make_aware(timezone.datetime.combine(sale.due_date, timezone.datetime.min.time())),
        message_template=message,
        generated_message=message
    )
