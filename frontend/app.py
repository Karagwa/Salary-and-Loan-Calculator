import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configure backend URL (will be overridden by Docker Compose)
BACKEND_URL = "http://backend:8000"

st.title("💰 Advanced Salary & Loan Calculator")

tab1, tab2 = st.tabs(["Salary Advance", "Loan Calculator"])

with tab1:
    st.header("Salary Advance Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        gross_salary = st.number_input("Gross Salary", min_value=0.0, step=100.0)
    with col2:
        pay_frequency = st.selectbox(
            "Pay Frequency",
            ["weekly", "bi-weekly", "monthly"]
        )
    
    requested_advance = st.number_input("Requested Advance Amount", min_value=0.0, step=100.0)
    
    if st.button("Calculate Advance"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/calculate_advance",
                json={
                    "gross_salary": gross_salary,
                    "pay_frequency": pay_frequency,
                    "requested_advance": requested_advance
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result['eligible']:
                    st.success("✅ You are eligible for this advance!")
                    st.write(f"Maximum available advance: ${result['max_available']:,.2f}")
                    st.write(f"Advance fee (5%): ${result['fee']:,.2f}")
                    st.write(f"Total repayment amount: ${result['total_repayment']:,.2f}")
                else:
                    st.error("❌ You are not eligible for this advance amount.")
                    st.write(f"Maximum available advance: ${result['max_available']:,.2f}")
            else:
                st.error("Error calculating advance. Please try again.")
                
        except requests.exceptions.RequestException:
            st.error("Backend service unavailable. Please try again later.")

with tab2:
    st.header("Loan Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input("Loan Amount", min_value=0.0, step=1000.0)
    with col2:
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
    
    loan_term = st.slider("Loan Term (months)", 1, 360, 12)
    
    if st.button("Calculate Loan"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/calculate_loan",
                json={
                    "amount": loan_amount,
                    "interest_rate": interest_rate,
                    "term": loan_term
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                st.success("Loan calculation complete!")
                st.write(f"Monthly payment: ${result['monthly_payment']:,.2f}")
                st.write(f"Total repayment: ${result['total_repayment']:,.2f}")
                st.write(f"Total interest: ${result['total_interest']:,.2f}")
                
                st.subheader("Amortization Schedule (First 12 Months)")
                schedule_df = pd.DataFrame(result['amortization_schedule'][:12])
                st.dataframe(schedule_df)
                
            else:
                st.error("Error calculating loan. Please try again.")
                
        except requests.exceptions.RequestException:
            st.error("Backend service unavailable. Please try again later.")

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configure backend URL (will be overridden by Docker Compose)
BACKEND_URL = "http://backend:8000"

st.title("💰 Advanced Salary & Loan Calculator")

tab1, tab2 = st.tabs(["Salary Advance", "Loan Calculator"])

with tab1:
    st.header("Salary Advance Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        gross_salary = st.number_input("Gross Salary", min_value=0.0, step=100.0)
    with col2:
        pay_frequency = st.selectbox(
            "Pay Frequency",
            ["weekly", "bi-weekly", "monthly"]
        )
    
    requested_advance = st.number_input("Requested Advance Amount", min_value=0.0, step=100.0)
    
    if st.button("Calculate Advance"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/calculate_advance",
                json={
                    "gross_salary": gross_salary,
                    "pay_frequency": pay_frequency,
                    "requested_advance": requested_advance
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result['eligible']:
                    st.success("✅ You are eligible for this advance!")
                    st.write(f"Maximum available advance: ${result['max_available']:,.2f}")
                    st.write(f"Advance fee (5%): ${result['fee']:,.2f}")
                    st.write(f"Total repayment amount: ${result['total_repayment']:,.2f}")
                else:
                    st.error("❌ You are not eligible for this advance amount.")
                    st.write(f"Maximum available advance: ${result['max_available']:,.2f}")
            else:
                st.error("Error calculating advance. Please try again.")
                
        except requests.exceptions.RequestException:
            st.error("Backend service unavailable. Please try again later.")

with tab2:
    st.header("Loan Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input("Loan Amount", min_value=0.0, step=1000.0)
    with col2:
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
    
    loan_term = st.slider("Loan Term (months)", 1, 360, 12)
    
    if st.button("Calculate Loan"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/calculate_loan",
                json={
                    "amount": loan_amount,
                    "interest_rate": interest_rate,
                    "term": loan_term
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                st.success("Loan calculation complete!")
                st.write(f"Monthly payment: ${result['monthly_payment']:,.2f}")
                st.write(f"Total repayment: ${result['total_repayment']:,.2f}")
                st.write(f"Total interest: ${result['total_interest']:,.2f}")
                
                st.subheader("Amortization Schedule (First 12 Months)")
                schedule_df = pd.DataFrame(result['amortization_schedule'][:12])
                st.dataframe(schedule_df)
                
            else:
                st.error("Error calculating loan. Please try again.")
                
        except requests.exceptions.RequestException:
            st.error("Backend service unavailable. Please try again later.")

st.sidebar.markdown("### System Status")
try:
    health = requests.get(f"{BACKEND_URL}/health").json()
    st.sidebar.success("Backend: Healthy")
except:
    st.sidebar.error("Backend: Unavailable")
