import joblib
import pandas as pd
from app.schemas import TransactionIn

# 1. Model Initialization
# Load the trained machine learning pipeline into memory on server startup.
MODEL_PATH = "model_training/fraud_model.joblib"
try:
    fraud_pipeline = joblib.load(MODEL_PATH)
    print("INFO: Machine learning model loaded successfully.")
except FileNotFoundError:
    fraud_pipeline = None
    print("WARNING: fraud_model.joblib not found. Ensure the training script has been executed.")

def calculate_fraud_risk(transaction: TransactionIn) -> dict:
    """Evaluates a transaction using the trained Scikit-Learn pipeline."""
    
    # Guard clause in case the model failed to load during startup
    if fraud_pipeline is None:
        return {"is_fraud": False, "fraud_probability": 0.0}

    # 2. Data Preparation
    # Convert the incoming Pydantic model to a Pandas DataFrame to maintain expected feature names.
    input_data = pd.DataFrame([{
        "transaction_amount": transaction.transaction_amount,
        "customer_age": transaction.customer_age
    }])

    # # 2. Data Preparation (Low-Latency Approach)
    # # We pass a 2D list. We MUST ensure the order strictly matches the training data.
    # input_data = [[
    #     transaction.transaction_amount, 
    #     transaction.customer_age
    # ]]

    # 3. Inference
    # Generate the discrete prediction and the continuous probability score.
    prediction = fraud_pipeline.predict(input_data)[0]
    probability_of_fraud = fraud_pipeline.predict_proba(input_data)[0][1]

    # 4. Response Formatting
    return {
        "account_id": transaction.account_id,
        "is_fraud": bool(prediction == 1),
        "fraud_probability": round(float(probability_of_fraud), 4)
    }