from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import AdvanceRequest, LoanRequest
from calculations import calculate_advance, calculate_loan
from calculations import router as calculations_router
import pandas as pd

app = FastAPI()

# CORS configuration to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)
#routers

app.include_router(calculations_router, prefix="/api", tags=["calculations"])



@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"msg": "Backend is alive!"}