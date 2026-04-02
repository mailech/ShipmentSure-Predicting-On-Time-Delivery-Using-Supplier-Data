from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

model = pickle.load(open('model.pkl', 'rb'))

warehouse_map  = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'F': 4}
shipment_map   = {'Flight': 0, 'Road': 1, 'Ship': 2}
importance_map = {'high': 0, 'low': 1, 'medium': 2}
gender_map     = {'F': 0, 'M': 1}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    features = [
        warehouse_map[data['warehouse_block']],
        shipment_map[data['mode_of_shipment']],
        int(data['customer_care_calls']),
        int(data['customer_rating']),
        int(data['cost_of_the_product']),
        int(data['prior_purchases']),
        importance_map[data['product_importance']],
        gender_map[data['gender']],
        int(data['discount_offered']),
        int(data['weight_in_gms']),
    ]

    prediction   = model.predict([features])[0]
    probability  = model.predict_proba([features])[0]

    on_time_prob = round(float(probability[1]) * 100, 1)
    delayed_prob = round(float(probability[0]) * 100, 1)
    confidence   = round(float(max(probability)) * 100, 1)
    reliability  = on_time_prob

    if delayed_prob < 35:
        risk_level = "Low"
    elif delayed_prob < 65:
        risk_level = "Medium"
    else:
        risk_level = "High"

    result = "✅ Delivered On Time" if prediction == 1 else "❌ Delayed"

    return jsonify({
        'prediction':        result,
        'on_time_probability': on_time_prob,
        'delayed_probability': delayed_prob,
        'confidence':        confidence,
        'reliability':       reliability,
        'risk_level':        risk_level,
    })

if __name__ == '__main__':
    app.run(debug=True)