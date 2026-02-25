import joblib
import pandas as pd
import pytest

MODEL_PATH = "model_training/fraud_model.joblib"

@pytest.fixture(scope="module")
def loaded_model():
    """Pytest fixture to load the serialized pipeline once per test session."""
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        pytest.fail("Model file not found. Run train_model.py first.")

def test_classifier_class_count(loaded_model):
    """
    Validates that the model was trained as a strict binary classifier.
    Prevents silent failures if dirty data introduces a third target class.
    """
    # Extract the final estimator from the Scikit-Learn pipeline
    # We access the named step "model" (or whatever name you gave the RandomForest in your training script)
    try:
        classifier_step = loaded_model.named_steps["model"]
    except KeyError:
        pytest.fail("Pipeline does not contain a step named 'model'.")
        
    # Assert the underlying model classes are exactly binary
    assert len(classifier_step.classes_) == 2

def test_amount_partial_dependence(loaded_model):
    """
    Test monotonicity: Holding age constant, increasing the transaction amount 
    should never decrease the probability of fraud.
    """
    constant_age = 25
    
    low_amount_data = pd.DataFrame([{"transaction_amount": 10.0, "customer_age": constant_age}])
    high_amount_data = pd.DataFrame([{"transaction_amount": 50000.0, "customer_age": constant_age}])
    
    low_risk_prob = loaded_model.predict_proba(low_amount_data)[0][1]
    high_risk_prob = loaded_model.predict_proba(high_amount_data)[0][1]
    
    assert high_risk_prob >= low_risk_prob

def test_age_partial_dependence(loaded_model):
    """
    Test monotonicity: Holding a high transaction amount constant, a significantly 
    younger customer should represent equal or higher risk based on our training data.
    """
    constant_amount = 15000.0
    
    older_customer_data = pd.DataFrame([{"transaction_amount": constant_amount, "customer_age": 60}])
    younger_customer_data = pd.DataFrame([{"transaction_amount": constant_amount, "customer_age": 18}])
    
    older_risk_prob = loaded_model.predict_proba(older_customer_data)[0][1]
    younger_risk_prob = loaded_model.predict_proba(younger_customer_data)[0][1]
    
    assert younger_risk_prob >= older_risk_prob