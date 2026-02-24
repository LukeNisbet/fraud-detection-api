from pydantic import BaseModel, Field

class TransactionIn(BaseModel):
    account_id: str
    transaction_amount: float = Field(gt=0, description="Amount must be greater than 0")
    merchant_category: str
    customer_age: int = Field(ge=18, le=120, description="Customer must be an adult")

class FraudPredictionOut(BaseModel):
    account_id: str
    fraud_probability: float
    is_fraud: bool