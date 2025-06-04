import pandas as pd
from datetime import datetime

def calculate_advance(gross_salary, pay_frequency, requested_advance):
    
    if pay_frequency == 'weekly':
        monthly_salary = gross_salary * 4.33
    elif pay_frequency == 'bi-weekly':
        monthly_salary = gross_salary * 2.166
    else:
        monthly_salary = gross_salary
    
    # Eligibility rules
    max_advance = monthly_salary * 0.3  # Max 30% of monthly salary
    is_eligible = requested_advance <= max_advance
    
    
    fee = requested_advance * 0.05 if is_eligible else 0
    
    return {
        "eligible": is_eligible,
        "requested_amount": requested_advance,
        "max_available": max_advance,
        "fee": round(fee, 2),
        "total_repayment": round(requested_advance + fee, 2) if is_eligible else 0
    }

def calculate_loan(amount, interest_rate, term):
    
    monthly_rate = interest_rate / 100 / 12
    payment = (monthly_rate * amount) / (1 - (1 + monthly_rate) ** -term)
    
    dates = pd.date_range(start=datetime.now(), periods=term, freq='M')
    schedule = pd.DataFrame(index=dates, columns=[
        'Payment', 'Principal', 'Interest', 'Remaining'
    ])
    
    remaining = amount
    for i in range(term):
        interest = remaining * monthly_rate
        principal = payment - interest
        remaining -= principal
        
        schedule.loc[dates[i], 'Payment'] = round(payment, 2)
        schedule.loc[dates[i], 'Principal'] = round(principal, 2)
        schedule.loc[dates[i], 'Interest'] = round(interest, 2)
        schedule.loc[dates[i], 'Remaining'] = round(remaining, 2) if remaining > 0 else 0
    
    total_interest = schedule['Interest'].sum()
    
    return {
        "monthly_payment": round(payment, 2),
        "total_repayment": round(amount + total_interest, 2),
        "total_interest": round(total_interest, 2),
        "amortization_schedule": schedule.to_dict('records')
    }