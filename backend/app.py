from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load model
try:
    model_path = "model.joblib"
    if not os.path.exists(model_path):
        model_path = "../model.joblib"

    model = joblib.load(model_path)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


@app.route('/api/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.json

    # Required fields
    required_fields = [
        'Warehouse_block', 'Mode_of_Shipment', 'Product_importance',
        'Customer_care_calls', 'Customer_rating',
        'Prior_purchases', 'Discount_offered', 'Weight_in_gms'
    ]

    for field in required_fields:
        if field not in data or data[field] in ['', None]:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        # Convert numeric values
        data['Customer_care_calls'] = int(data['Customer_care_calls'])
        data['Customer_rating'] = int(data['Customer_rating'])
        data['Prior_purchases'] = int(data['Prior_purchases'])
        data['Discount_offered'] = int(data['Discount_offered'])
        data['Weight_in_gms'] = int(data['Weight_in_gms'])

        # Basic sanity checks
        if data['Customer_rating'] < 1 or data['Customer_rating'] > 5:
            return jsonify({"error": "Customer rating must be between 1 and 5"}), 400

        if data['Weight_in_gms'] <= 0:
            return jsonify({"error": "Weight must be positive"}), 400

        # Create DataFrame
        df = pd.DataFrame([data])

        # Get probabilities
        probs = model.predict_proba(df)[0]
        prob_delayed = float(probs[0])
        prob_on_time = float(probs[1])

        # Prediction (robust)
        prediction_text = "DELAYED" if prob_delayed >= prob_on_time else "ON TIME"

        # Display probability (confidence in prediction)
        display_prob = prob_delayed if prediction_text == "DELAYED" else prob_on_time

        # Confidence level
        if display_prob > 0.8:
            confidence = "High"
        elif display_prob > 0.6:
            confidence = "Medium"
        else:
            confidence = "Low"

        # Risk level (based on delay probability)
        if prob_delayed < 0.3:
            risk_level = "Low"
        elif prob_delayed < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return jsonify({
            "probability": round(display_prob, 4),
            "prediction": prediction_text,
            "confidence": confidence,
            "risk_level": risk_level
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)