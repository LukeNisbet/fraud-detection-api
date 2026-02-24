from fastapi import FastAPI
from app.schemas import TransactionIn, FraudPredictionOut

# Initialize the API application
app = FastAPI(title="Fraud Detection API")

# 1. The Health Check (GET)
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Fraud API is running!"}

# 2. The Machine Learning Endpoint (POST)
@app.post("/predict", response_model=FraudPredictionOut)
def predict_fraud(transaction: TransactionIn):
    
    # MOCK ML LOGIC: We will replace this with a real model later
    risk_score = 0.05
    
    # Simple rule-based logic for now
    if transaction.transaction_amount > 10000:
        risk_score += 0.60
    if transaction.customer_age < 25:
        risk_score += 0.20
        
    is_fraud = risk_score > 0.50
    
    # Return a dictionary that matches the FraudPredictionOut schema
    return {
        "account_id": transaction.account_id,
        "fraud_probability": risk_score,
        "is_fraud": is_fraud
    }