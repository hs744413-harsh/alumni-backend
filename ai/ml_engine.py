import joblib
import pandas as pd

# load your trained model
model = joblib.load("models/recommender.pkl")

def predict_match(input_dict: dict):
    df = pd.DataFrame([input_dict])
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]
    return {"prediction": int(pred), "confidence": float(prob)}