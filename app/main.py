from fastapi import FastAPI
from app.schemas import TransactionIn, FraudPredictionOut
from app.model import calculate_fraud_risk  # Import our business logic

app = FastAPI(title="Fraud Detection API")

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Fraud API is running!"}

@app.post("/predict", response_model=FraudPredictionOut)
def predict_fraud(transaction: TransactionIn):
    # The web server just hands the data to the model and returns the result
    return calculate_fraud_risk(transaction)