from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
import os

app = FastAPI(title="AI ShipmentSure API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'best_model.pkl')
PREPROCESSOR_PATH = os.path.join(BASE_DIR, 'models', 'preprocessor.pkl')

# Global variables for model and preprocessor
model = None
preprocessor = None

@app.on_event("startup")
async def load_model_and_preprocessor():
    global model, preprocessor
    try:
        if not os.path.exists(MODEL_PATH):
            print(f"Model not found at {MODEL_PATH}")
            return
        
        if not os.path.exists(PREPROCESSOR_PATH):
            print(f"Preprocessor not found at {PREPROCESSOR_PATH}")
            return

        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        with open(PREPROCESSOR_PATH, 'rb') as f:
            preprocessor = pickle.load(f)
            
        print("Model and preprocessor loaded successfully.")
    except Exception as e:
        print(f"Error loading artifacts: {e}")

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

@app.get("/")
def read_root():
    return {"message": "Welcome to AI ShipmentSure API"}

@app.get("/status")
def get_status():
    if model is not None and preprocessor is not None:
        return {"status": "ready", "model": "loaded"}
    else:
        return {"status": "error", "message": "Model or preprocessor not loaded"}

@app.post("/predict")
async def predict_delivery(shipment: ShipmentInput):
    if model is None or preprocessor is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")

    try:
        # Create a DataFrame for the input
        input_data = pd.DataFrame([{
            'Warehouse_block': shipment.Warehouse_block,
            'Mode_of_Shipment': shipment.Mode_of_Shipment,
            'Customer_care_calls': shipment.Customer_care_calls,
            'Customer_rating': shipment.Customer_rating,
            'Cost_of_the_Product': shipment.Cost_of_the_Product,
            'Prior_purchases': shipment.Prior_purchases,
            'Product_importance': shipment.Product_importance,
            'Gender': shipment.Gender,
            'Discount_offered': shipment.Discount_offered,
            'Weight_in_gms': shipment.Weight_in_gms
        }])

        # Transform data using preprocessor
        input_processed = preprocessor.transform(input_data)
        
        # Predict
        prediction = int(model.predict(input_processed)[0])
        probability = model.predict_proba(input_processed)[0]
        
        # Prediction: 1 means Reached on Time, 0 means NOT Reached on Time (Delayed)
        status = "On Time" if prediction == 1 else "Delayed"
        confidence = float(max(probability))

        return {
            "prediction": prediction,
            "status": status,
            "confidence": confidence,
            "probability": probability.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during prediction: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
