from fastapi.testclient import TestClient
from app.model import calculate_fraud_risk
from app.main import app
from app.schemas import TransactionIn, FraudPredictionOut
from pydantic import ValidationError
import pytest

# Integration tests
# Create our fake "browser" to fire requests at our API
client = TestClient(app)

def test_predict_fraud_success():
    """Test that valid data returns a 200 OK and correct calculations."""
    payload = {
        "account_id": "ACC123",
        "transaction_amount": 15000.0,
        "customer_age": 22
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["is_fraud"] == True
    assert response.json()["account_id"] == "ACC123"

def test_predict_fraud_validation_error():
    """Test that Pydantic successfully blocks bad data."""
    payload = {
        "account_id": "ACC999",
        "transaction_amount": -500.0,  # Pydantic should catch this!
        "customer_age": 30
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

# Unit Tests
def test_model_logic():
    # Create a Pydantic object
    test_tx = TransactionIn(
        account_id= "ACC999",
        transaction_amount= 500.0,
        customer_age= 30
    )

    result = calculate_fraud_risk(test_tx)
    assert result["is_fraud"] == False
    assert result["fraud_probability"] == 0.05


# Validation Tests
def test_customer_age_validation():
    # ARRANGE: We know the age is 12, which violates the ge=18 rule
    
    # ACT & ASSERT: We wrap the action in pytest.raises
    with pytest.raises(ValidationError) as error_info:
        TransactionIn(
            account_id="ACC999",
            transaction_amount=500.0,
            customer_age=12
        )
    
    # Bonus Assert: We can even peek inside the crash to make sure it crashed for the right reason!
    assert "greater than or equal to 18" in str(error_info.value)