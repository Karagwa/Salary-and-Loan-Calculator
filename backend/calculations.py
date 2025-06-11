import pandas as pd
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from models import AdvanceRequest, LoanRequest

router= APIRouter()



@router.post("/calculate_advance", response_class=dict)
def calculate_advance(data: AdvanceRequest):
    
    if data.pay_frequency == 'weekly':
        monthly_salary = data.gross_salary * 4.33
    elif data.pay_frequency == 'bi-weekly':
        monthly_salary = data.gross_salary * 2.166
    else:
        monthly_salary = data.gross_salary
    
    # Eligibility rules
    max_advance = monthly_salary * 0.3  # Max 30% of monthly salary
    is_eligible = data.requested_advance <= max_advance
    
    
    fee = data.requested_advance * 0.05 if is_eligible else 0
    
    return {
        "eligible": is_eligible,
        "requested_amount": data.requested_advance,
        "max_available": max_advance,
        "fee": round(fee, 2),
        "total_repayment": round(data.requested_advance + fee, 2) if is_eligible else 0
    }

@router.post("/calculate_loan", response_class=dict)
def calculate_loan(data: LoanRequest):
    amount = data.amount
    interest_rate = data.interest_rate
    term = data.term  # in months
    
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