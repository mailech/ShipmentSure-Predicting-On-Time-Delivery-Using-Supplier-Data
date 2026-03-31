from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = joblib.load("models/model_pipeline.pkl")

# ---------- HEALTH API ----------
@app.get("/health")
def health():
    return {"status": "ok", "project": "ShipmentSure"}


# ---------- SCHEMA API ----------
@app.get("/schema")
def schema():
    return {
        "raw_fields": [
            {"name": "ID", "type": "number", "default": 5000, "min": 1, "max": 11000},
            {"name": "Warehouse_block", "type": "select", "options": ["A","B","C","D","F"], "default": "A"},
            {"name": "Mode_of_Shipment", "type": "select", "options": ["Flight","Road","Ship"], "default": "Flight"},
            {"name": "Customer_care_calls", "type": "number", "default": 4, "min": 1, "max": 10},
            {"name": "Customer_rating", "type": "number", "default": 3, "min": 1, "max": 5},
            {"name": "Cost_of_the_Product", "type": "number", "default": 200, "min": 50, "max": 500},
            {"name": "Prior_purchases", "type": "number", "default": 3, "min": 1, "max": 10},
            {"name": "Product_importance", "type": "select", "options": ["low","medium","high"], "default": "low"},
            {"name": "Gender", "type": "select", "options": ["M","F"], "default": "M"},
            {"name": "Discount_offered", "type": "number", "default": 5, "min": 0, "max": 70},
            {"name": "Weight_in_gms", "type": "number", "default": 3000, "min": 1000, "max": 8000}
        ]
    }


# ---------- ENCODING ----------
def preprocess(data):
    df = pd.DataFrame([data])

    # One-hot encoding same as training
    df = pd.get_dummies(df)

    # Ensure all columns exist
    expected_cols = model[0].feature_names_in_ if isinstance(model, tuple) else df.columns

    for col in expected_cols:
        if col not in df:
            df[col] = 0

    df = df[expected_cols]

    return df


# ---------- PREDICTION API ----------
@app.post("/predict")
def predict(data: dict):
    try:
        df = preprocess(data)

        if isinstance(model, tuple):
            scaler, clf = model
            df = scaler.transform(df)
            prediction = clf.predict(df)[0]
            prob = clf.predict_proba(df)[0]
        else:
            prediction = model.predict(df)[0]
            prob = model.predict_proba(df)[0]

        return {
            "prediction": int(prediction),
            "prediction_label": "On Time" if prediction == 0 else "Late",
            "confidence": float(np.max(prob)),
            "class_probabilities": {
                "0": float(prob[0]),
                "1": float(prob[1])
            },
            "message": "Prediction successful"
        }

    except Exception as e:
        return {"error": str(e)}
    


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Serve frontend
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_PATH = os.path.join(BASE_DIR, "..", "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

INDEX_PATH = os.path.join(FRONTEND_PATH, "index.html")

@app.get("/")
def home():
    return FileResponse(INDEX_PATH)