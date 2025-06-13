import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configure backend URL (will be overridden by Docker Compose)
BACKEND_URL = "https://fastapi-backend-service-77068367626.us-central1.run.app"

st.title("💰 Advanced Salary & Loan Calculator")

st.subheader("Welcome to the Advanced Salary and Loan Calculator App!")
st.markdown("""
            This app allows you to calculate your eligibility for a salary advance and provides a loan calculator to help you manage your finances effectively.
            Choose a tab below to get started!
            """)

tab1, tab2 = st.tabs(["Salary Advance Calculator", "Loan Calculator"])

with tab1:
    st.header("Salary Advance Calculator")
    st.markdown("""
                This tool helps you determine if you are eligible for a salary advance and calculates the maximum available amount based on your gross salary and pay frequency.""")
    
    col1, col2 = st.columns(2)
    with col1:
        gross_salary = st.number_input("Gross Salary",placeholder="Enter your gross salary", min_value=0.0, step=100.0)
        st.caption("This is your total salary before any deductions.")
    with col2:
        pay_frequency = st.selectbox(
            "Pay Frequency",
            ["weekly", "bi-weekly", "monthly"]
        )
        st.caption("This is the frequency at which you receive your salary.")
    
    requested_advance = st.number_input("Requested Advance Amount", placeholder="Enter the amount ", min_value=0.0, step=100.0)
    st.caption("This is the amount you wish to request as an advance on your salary.")
    
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
    st.subheader("Calculate your monthly payments and total repayment for a loan.")
    
    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input("Loan Amount", placeholder="Enter loan amount", min_value=0.0, step=1000.0)
        st.caption("This is the total amount you wish to borrow.")
    with col2:
        interest_rate = st.number_input("Interest Rate (%)",placeholder="Enter interest rate", min_value=0.0, max_value=100.0, step=0.1)
        st.caption("This is the annual interest rate for the loan.")
    loan_term = st.slider("Loan Term (months)", 1, 360, 12)
    st.caption("This is the duration of the loan in months. Choose between 1 month and 30 years (360 months).")
    st.markdown("""
                The loan calculator will compute your monthly payment, total repayment amount, and total interest paid over the life of the loan.
                It will also provide an amortization schedule for the first 12 months of the loan.
                """)
    
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
                
                st.subheader(f"Amortization Schedule ({loan_term} Months)")
                
                schedule_df = pd.DataFrame(result['amortization_schedule'][:loan_term])
                st.dataframe(schedule_df)
                st.markdown("""
                            The amortization schedule shows the breakdown of each payment into principal and interest, along with the remaining balance.

                            """)
                st.caption("What is an amortization schedule? It is a table that details each periodic payment on a loan, showing how much goes towards interest and how much goes towards the principal balance.")
                
                st.write("Generated on:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                st.error("Error calculating loan. Please try again.")
                
        except requests.exceptions.RequestException:
            st.error("Backend service unavailable. Please try again later.")


