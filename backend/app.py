from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "templates"))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "static"))


MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "models", "best_xgb.pkl"))

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print("✅ Model loaded successfully")
print("Model type:", type(model))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # -------------------------------
        # SAFE CONVERSION FUNCTIONS
        # -------------------------------
        def to_float(val):
            try:
                return float(val)
            except:
                return 0.0


        input_df = pd.DataFrame([{
            "Warehouse_block": data.get("warehouse"),
            "Mode_of_Shipment": data.get("mode"),
            "Customer_care_calls": to_float(data.get("calls")),
            "Customer_rating": to_float(data.get("rating")),
            "Cost_of_the_Product": to_float(data.get("cost")),
            "Prior_purchases": to_float(data.get("purchases")),
            "Product_importance": data.get("importance"),
            "Gender": data.get("gender"),
            "Discount_offered": to_float(data.get("discount")),
            "Weight_in_gms": to_float(data.get("weight"))
        }])

        print("\n📥 Incoming Data:")
        print(input_df)


        prediction = model.predict(input_df)[0]


        try:
            prob = model.predict_proba(input_df)[0][1]
            confidence = f"{round(prob * 100, 2)}%"
        except:
            confidence = "N/A"

        result = "On Time" if prediction == 1 else "Delayed"

        return jsonify({
            "prediction": result,
            "confidence": confidence
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)