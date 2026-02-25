import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. DATA PREPARATION: Create historical data and split into clues (X) and answers (y)
data = {
    "transaction_amount": [50.0, 15000.0, 20.0, 8000.0, 5.0, 25000.0, 100.0, 12000.0],
    "customer_age": [35, 22, 45, 19, 30, 18, 55, 21],
    "is_fraud": [0, 1, 0, 1, 0, 1, 0, 1]  # 0 = Safe, 1 = Fraud
}
df = pd.DataFrame(data)

X = df[["transaction_amount", "customer_age"]]  # The features (inputs)
y = df["is_fraud"]                              # The target (outputs)

# 2. PIPELINE SETUP: Build the sequence of transformations and the algorithm
print("Building the pipeline...")
fraud_pipeline = Pipeline(steps=[
    ("scaler", StandardScaler()),                       # Step 1: Normalize the numbers
    ("model", RandomForestClassifier(random_state=42))  # Step 2: The ML Brain
])

# 3. MODEL TRAINING: Feed the data through so the algorithm learns the patterns
print("Training the model...")
fraud_pipeline.fit(X, y)

# 4. SERIALIZATION: Freeze the trained brain into a physical file for the API to use later
save_path = "model_training/fraud_model.joblib"
joblib.dump(fraud_pipeline, save_path)
print(f"Success! Model saved to disk as '{save_path}'")