from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from calculations import calculate_advance, calculate_loan
import pandas as pd

app = FastAPI()

# CORS configuration to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class AdvanceRequest(BaseModel):
    gross_salary: float
    pay_frequency: str  # 'weekly', 'bi-weekly', 'monthly'
    requested_advance: float

class LoanRequest(BaseModel):
    amount: float
    interest_rate: float
    term: int  

@app.post("/calculate_advance")
async def process_advance(request: AdvanceRequest):
    return calculate_advance(
        request.gross_salary,
        request.pay_frequency,
        request.requested_advance
    )

@app.post("/calculate_loan")
async def process_loan(request: LoanRequest):
    return calculate_loan(
        request.amount,
        request.interest_rate,
        request.term
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"msg": "Backend is alive!"}