from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Load trained pipeline model
model = pickle.load(open("FINAL_MODEL.pkl", "rb"))

print("MODEL TYPE:", type(model))


# 📥 Input schema
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


# 🏠 Home route
@app.get("/")
def home():
    return {"message": "Shipment API Running 🚀"}


# 🚀 Prediction API
@app.post("/predict")
def predict(data: ShipmentInput):
    try:
        # Convert input → DataFrame
        df = pd.DataFrame([data.dict()])

        # Ensure correct order
        df = df[[
            'Warehouse_block',
            'Mode_of_Shipment',
            'Customer_care_calls',
            'Customer_rating',
            'Cost_of_the_Product',
            'Prior_purchases',
            'Product_importance',
            'Gender',
            'Discount_offered',
            'Weight_in_gms'
        ]]

        # 🔍 Extract values
        discount = df['Discount_offered'].iloc[0]
        weight = df['Weight_in_gms'].iloc[0]
        rating = df['Customer_rating'].iloc[0]
        calls = df['Customer_care_calls'].iloc[0]

        # 🔴 Rule-based check
        if (
            (discount >= 70 and weight >= 3000) or
            (rating <= 2 and calls >= 4)
        ):
            status = "Delayed ❌"
            confidence = 0.9

        else:
            # 🤖 ML Prediction
            prob = model.predict_proba(df)[0]
            on_time_prob = prob[1]

            if on_time_prob >= 0.5:
                status = "On Time ✅"
            else:
                status = "Delayed ❌"

            confidence = float(on_time_prob)

        # 🧠 Confidence classification
        conf_percent = round(confidence * 100)

        if conf_percent < 50:
            conf_label = "Low Confidence ❌"
        elif conf_percent < 70:
            conf_label = "Moderate ⚠️"
        elif conf_percent < 90:
            conf_label = "High Confidence ✅"
        else:
            conf_label = "Very Strong 🔥"

        return {
            "status": status,
            "confidence_percent": f"{conf_percent}%",
            "confidence_level": conf_label
        }

    except Exception as e:
        return {"error": str(e)}