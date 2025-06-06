from src import bcrypt
from datetime import datetime, timedelta


def generate_pw_hash(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_pw_hash(password, hash):
    return bcrypt.check_password_hash(hash, password)

def update_welfare_payment_dates(welfare_payment):
    """
    Updates the last_paid_date and calculates the next_due_date for a WelfarePayment.
    """
    if welfare_payment.next_due_date:
        welfare_payment.last_paid_date = welfare_payment.next_due_date

    today = datetime.now().date()

    if welfare_payment.frequency == 'monthly':
        # Calculate next month's date, handling month rollovers
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        welfare_payment.next_due_date = next_month - timedelta(days=1)
    elif welfare_payment.frequency == 'weekly':
        welfare_payment.next_due_date = today + timedelta(weeks=1)
    elif welfare_payment.frequency == 'bi-weekly':
        welfare_payment.next_due_date = today + timedelta(weeks=2)
    elif welfare_payment.frequency == 'yearly':
        welfare_payment.next_due_date = today.replace(year=today.year + 1)
    else:
        raise ValueError(f"Unrecognized frequency: {welfare_payment.frequency}")
