from fastapi import APIRouter
from app.schemas import TransactionIn, FraudPredictionOut
from app.model import calculate_fraud_risk

router = APIRouter()

@router.post("/predict", response_model=FraudPredictionOut) #this maps the "/predict" URL to the predict_fraud function
def predict_fraud(transaction: TransactionIn):
    return calculate_fraud_risk(transaction)