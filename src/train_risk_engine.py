import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Synthetic training data
X = np.array([
    [1, 3.5, 0, 0, 10],   # clean
    [2, 4.0, 0, 0, 20],
    [4, 4.8, 1, 1, 50],   # suspicious
    [6, 5.5, 3, 2, 120],
    [8, 6.2, 5, 3, 200], # malicious
    [9, 6.8, 7, 4, 300]
])

y = np.array([
    0, 0,   # Low
    1, 1,   # Medium
    2, 2    # High
])

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "models/risk_model.pkl")
print("[+] Risk model trained & saved")

