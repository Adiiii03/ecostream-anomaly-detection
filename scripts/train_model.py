import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# 1. Generate "Normal" Data for Training
# We want the model to learn that ~50°C and ~100 Pressure is "Safe"
print("Generatng synthetic training data...")
n_samples = 1000

data = {
    "temperature": np.random.normal(50, 5, n_samples),  # Mean 50, Std 5
    "pressure": np.random.normal(100, 10, n_samples),   # Mean 100, Std 10
    "vibration": np.random.normal(10, 2, n_samples)     # Mean 10, Std 2
}

df = pd.DataFrame(data)

# 2. Train the Model (Isolation Forest)
# contamination=0.01 means we expect ~1% of new data to be anomalies
print("Training Isolation Forest model...")
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(df)

# 3. Save the "Brain"
# We save the trained model to a file so our API can load it later
joblib.dump(model, "isolation_forest.pkl")
print("✅ Model trained and saved as 'isolation_forest.pkl'")

# 4. Test it immediately
print("\n--- Testing Model ---")
test_normal = [[50, 100, 10]]   # Should be 1 (Normal)
test_anomaly = [[120, 300, 90]] # Should be -1 (Anomaly)

pred_normal = model.predict(test_normal)
pred_anomaly = model.predict(test_anomaly)

print(f"Normal Reading {test_normal} -> Prediction: {pred_normal[0]} (1 is Normal)")
print(f"Danger Reading {test_anomaly} -> Prediction: {pred_anomaly[0]} (-1 is Anomaly)")