
# 💰 Advanced Salary & Loan Calculator

A Dockerized microservice application with Streamlit frontend and FastAPI backend for financial calculations.

## 🔧 Project Overview & Architecture

**Key Features:**
- Salary advance eligibility calculator
- Loan repayment simulator with amortization schedule
- Containerized deployment with Docker Compose

**System Architecture:**
```
┌─────────────────────┐    HTTP Requests    ┌─────────────────────┐
│                     │◄───────────────────►│                     │
│  Streamlit Frontend │                     │  FastAPI Backend    │
│  (Port 8501)        │    JSON Responses   │  (Port 8000)        │
└─────────────────────┘                     └─────────────────────┘
        ▲                                           ▲
        │                                           │
        │                                           │
        ▼                                           ▼
┌─────────────────────┐                     ┌─────────────────────┐
│      User           │                     │   Pandas Engine      │
│   (Web Browser)     │                     │  (Calculations)      │
└─────────────────────┘                     └─────────────────────┘
```

## 🚀 API Endpoint Documentation

### `POST /calculate_advance`
**Request:**
```json
{
  "gross_salary": 5000.00,
  "pay_frequency": "monthly",
  "requested_advance": 1500.00
}
```

**Response:**
```json
{
  "eligible": true,
  "requested_amount": 1500.00,
  "max_available": 1500.00,
  "fee": 75.00,
  "total_repayment": 1575.00
}
```

### `POST /calculate_loan`
**Request:**
```json
{
  "amount": 10000.00,
  "interest_rate": 5.5,
  "term": 24
}
```

**Response:**
```json
{
  "monthly_payment": 440.96,
  "total_repayment": 10583.04,
  "total_interest": 583.04,
  "amortization_schedule": [
    {
      "date": "2023-11-01",
      "payment": 440.96,
      "principal": 396.04,
      "interest": 44.92,
      "remaining": 9603.96
    },
    ...
  ]
}
```

## 📊 Pandas Financial Engine

The backend leverages Pandas for:
1. **Amortization Schedule Generation**:
```python
dates = pd.date_range(start=datetime.now(), periods=term, freq='M')
schedule = pd.DataFrame(index=dates, columns=[
    'Payment', 'Principal', 'Interest', 'Remaining'
])
```

2. **Compound Interest Calculations**:
```python
monthly_rate = interest_rate / 100 / 12
payment = (monthly_rate * amount) / (1 - (1 + monthly_rate) ** -term)
```

3. **Efficient Data Aggregation**:
```python
total_interest = schedule['Interest'].sum()
```

## 🛠️ Setup & Deployment

### Local Development
```bash
# Clone repository
git clone https://github.com/Karagwa/Salary-and-Loan-Calculator


# Build and run containers
docker compose up --build

# Access services:
# Frontend: http://localhost:8501
# Backend Docs: http://localhost:8000/docs
```



## 🔍 Key Assumptions

**Salary Advance:**
- Maximum advance = 30% of monthly salary equivalent
- 5% processing fee on advance amount
- Pay frequency conversions:
  - Weekly → Monthly: ×4.33
  - Bi-weekly → Monthly: ×2.166

**Loan Calculator:**
- Standard amortizing loan formula
- Monthly compounding interest
- Fixed rate for entire term
- No additional fees or penalties

## 🌍 Live Deployment

Access the production deployment at:  


## 📜 License
MIT License - See [LICENSE](LICENSE) for details

---


```