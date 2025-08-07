# scripts/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load dataset
df = pd.read_csv("data/labeled_can_data.csv")

# Drop timestamp if present
if 'timestamp' in df.columns:
    df = df.drop(columns=['timestamp'])

# Split features and labels
X = df.drop(columns=['label'])
y = df['label']

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ✅ Ensure 'model/' folder exists
os.makedirs("model", exist_ok=True)

# Save the trained model
joblib.dump(model, "model/can_intrusion_model.pkl")

print("✅ Model trained and saved successfully.")
