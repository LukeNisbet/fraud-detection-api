# Real-Time Fraud Detection ML API

A production-ready REST API that serves a Scikit-Learn machine learning pipeline for real-time credit card fraud detection.

This project demonstrates the transition from a static data science model into a deployable software engineering asset, utilizing FastAPI for the web layer, Pydantic for strict data validation, and Pytest for behavioral and systemic testing.

## Architecture & Design Patterns

- **Separation of Concerns:** The routing layer (`APIRouter`) is completely decoupled from the machine learning inference logic, preventing circular imports and allowing for modular scaling.
- **Strict Schema Validation:** Incoming transaction data is validated at runtime using Pydantic, rejecting malformed or logically impossible payloads (e.g., negative transaction amounts, underage customers) before they reach the model.
- **Feature Alignment:** Incoming payloads are mapped to Pandas DataFrames prior to inference, guaranteeing that the mathematical model receives the exact feature names and sequence it expects.
- **MLOps Testing:** The test suite is divided into integration tests for the API layer and isolated statistical/behavioral tests for the serialized `.joblib` model (testing partial dependence and probability bounds).

## Tech Stack

- **Web Framework:** FastAPI, Uvicorn
- **Data Validation:** Pydantic
- **Machine Learning:** Scikit-Learn, Pandas, Joblib
- **Testing:** Pytest

## Project Structure

```text
├── app/
│   ├── main.py          # Application entry point and global configurations
│   ├── api.py           # API routing and endpoint definitions
│   ├── model.py         # Model initialization and inference logic
│   └── schemas.py       # Pydantic data validation schemas
├── model_training/      #This would normally be a different repo
│   ├── train_model.py   # Training script and pipeline generation
│   └── test_model.py    # Statistical and behavioral tests for the ML model
├── tests/
│   └── test_main.py     # Integration and unit tests for the API endpoints
├── requirements.txt     # Locked production dependencies
└── README.md
```

## Running the API Locally

1. **Activate your virtual environment** and install the exact project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. **Train the machine learning model** (Generates the `.joblib` artifact):

   ```bash
   python model_training/train_model.py
   ```

3. **Start the local server:**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the interactive documentation:**
   Navigate to `http://localhost:8000/docs` to test the `/predict` endpoint.

## Running the Test Suite

Execute the entire test suite, covering both API validation and ML behavioral logic:

```bash
pytest
```
