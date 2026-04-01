from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import pickle
import os

app = FastAPI(title="ShipmentSure API")

# -------------------------------
# CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# PATH SETUP (FIXED)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Static files (CSS + JS)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")),
    name="static"
)

# -------------------------------
# LOAD MODEL + PREPROCESSOR
# -------------------------------
model = None
preprocessor = None

@app.on_event("startup")
def load_files():
    global model, preprocessor

    try:
        model_path = os.path.join(MODEL_DIR, "best_xgb.pkl")
        preprocessor_path = os.path.join(MODEL_DIR, "preprocessor.pkl")

        if not os.path.exists(model_path):
            print("❌ Model not found:", model_path)
        else:
            with open(model_path, "rb") as f:
                model = pickle.load(f)

        if not os.path.exists(preprocessor_path):
            print("❌ Preprocessor not found:", preprocessor_path)
        else:
            with open(preprocessor_path, "rb") as f:
                preprocessor = pickle.load(f)

        print("✅ Model & Preprocessor Loaded")

    except Exception as e:
        print("❌ Error loading files:", e)

# -------------------------------
# INPUT SCHEMA
# -------------------------------
class ShipmentInput(BaseModel):
    Warehouse_block: str
    Mode_of_Shipment: str
    Customer_care_calls: int
    Customer_rating: int
    Cost_of_the_Product: float
    Prior_purchases: int
    Product_importance: str
    Gender: str
    Discount_offered: float
    Weight_in_gms: float

# -------------------------------
# ROUTES
# -------------------------------

# ✅ Serve HTML (NO JINJA)
@app.get("/")
def home():
    file_path = os.path.join(FRONTEND_DIR, "templates", "index.html")
    return FileResponse(file_path)

# Status check
@app.get("/status")
def status():
    return {
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None
    }

# Prediction API
@app.post("/predict")
def predict(data: ShipmentInput):
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Model or preprocessor not loaded")

    try:
        # Convert input to DataFrame
        df = pd.DataFrame([data.dict()])

        # Apply preprocessing
        processed = preprocessor.transform(df)

        # Predict
        prediction = int(model.predict(processed)[0])

        # Confidence
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(processed)[0]
            confidence = float(max(prob))
        else:
            confidence = None

        result = "On Time ✅" if prediction == 1 else "Delayed ❌"

        return {
            "prediction": result,
            "confidence": confidence
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)