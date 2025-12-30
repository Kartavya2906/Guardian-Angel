import numpy as np
import joblib
import os

LABELS = {0: "Low", 1: "Medium", 2: "High"}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model.pkl")

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError("risk_model.pkl missing")
    return joblib.load(MODEL_PATH)

def build_features(behavior_score, crypto, lines):
    return np.array([[
        behavior_score,
        crypto["avg_entropy"],
        crypto["high_entropy_lines"],
        crypto["base64_payload_count"],
        lines
    ]])

def predict(model, features):
    pred = model.predict(features)[0]
    conf = max(model.predict_proba(features)[0])
    return {"risk": LABELS[pred], "confidence": round(conf, 2)}

