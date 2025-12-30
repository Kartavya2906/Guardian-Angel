import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

os.makedirs("models", exist_ok=True)

# Synthetic training data
X = np.array([
    [1, 3.5, 0, 0, 10],
    [2, 4.0, 0, 0, 20],
    [4, 4.8, 1, 1, 50],
    [6, 5.5, 3, 2, 120],
    [8, 6.2, 5, 3, 200],
    [9, 6.8, 7, 4, 300]
])

# Labels: 0=Low, 1=Medium, 2=High
y = np.array([0, 0, 1, 1, 2, 2])

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "models/risk_model.pkl")

print("[+] risk_model.pkl created successfully")

