from pydantic import BaseModel

class AdvanceRequest(BaseModel):
    gross_salary: float
    pay_frequency: str  # 'weekly', 'bi-weekly', 'monthly'
    requested_advance: float

class LoanRequest(BaseModel):
    amount: float
    interest_rate: float
    term: int  