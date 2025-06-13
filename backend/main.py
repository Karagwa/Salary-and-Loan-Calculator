from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import AdvanceRequest, LoanRequest
from calculations import calculate_advance, calculate_loan
from calculations import router as calculations_router
import pandas as pd

app = FastAPI()

origins = [
    "https://streamlit-frontend-service-77068367626.us-central1.run.app", # <--- REPLACE THIS with your actual Streamlit URL
    "http://localhost:8501",  # Allow requests from your local Streamlit development server
    "http://localhost:8000",  # Allow requests from your local FastAPI development server (if needed)
    # You can add more origins here if your frontend might be deployed elsewhere (e.g., a custom domain later)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of origins that are allowed to make requests
    allow_credentials=True,         # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Allow all headers in cross-origin requests
)

app.include_router(calculations_router, tags=["calculations"])



@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"msg": "Backend is alive!"}