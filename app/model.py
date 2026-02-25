from app.schemas import TransactionIn

def calculate_fraud_risk(transaction: TransactionIn) -> dict:
    """
    This function acts as our mock Machine Learning model.
    It takes a validated transaction and returns a risk assessment.
    """
    risk_score = 0.05
    
    # Simple rule-based logic
    if transaction.transaction_amount > 10000:
        risk_score += 0.60
    if transaction.customer_age < 25:
        risk_score += 0.20
        
    is_fraud = risk_score > 0.50
    
    # Return the exact dictionary shape our API promised
    return {
        "account_id": transaction.account_id,
        "fraud_probability": risk_score,
        "is_fraud": is_fraud
    }