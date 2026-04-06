# 📦 ShipmentSure: AI-Powered Delivery Prediction

[![Deployment Status](https://img.shields.io/badge/Deployment-Live-brightgreen)](https://shipmentsure-predicting-on-time-delivery-cvr4.onrender.com)
[![Tech Stack](https://img.shields.io/badge/Stack-React%20%7C%20Flask%20%7C%20XGBoost-blue)](https://shipmentsure-predicting-on-time-delivery-cvr4.onrender.com)

**ShipmentSure** is a sophisticated machine learning application designed to predict whether a shipment will be delivered on time or delayed based on supplier and logistics data. Featuring a premium **Neobrutalist UI**, it provides real-time predictions and deep model insights to help logistics managers optimize their supply chain.

🚀 **Live Demo:** [ShipmentSure on Render](https://shipmentsure-predicting-on-time-delivery-cvr4.onrender.com)

---

## ✨ Key Features

- **🎯 Precision Prediction**: Leverages a highly calibrated XGBoost model to predict "Delayed" vs. "On Time" status with confidence levels.
- **📊 Model Insights**: Interactive dashboard showing feature importance and data distributions (e.g., Warehouse Block performance, Discount impacts).
- **⚡ Real-time Interface**: Built with React and Vite for a lightning-fast, responsive user experience.
- **🎨 Premium Design**: A unique Neobrutalist aesthetic that emphasizes clarity, bold typography, and interactive elements.
- **🛠️ Robust Backend**: Flask-based API that handles model inference and data processing efficiently.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React, Vite, TailwindCSS, Lucide Icons, Framer Motion |
| **Backend** | Flask (Python), Pandas, Gunicorn |
| **Machine Learning** | XGBoost, Scikit-learn, Joblib |
| **Deployment**| Render (Full Stack) |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```text
.
├── backend/                # Flask API & Model Logic
│   ├── app.py              # Main API entry point
│   ├── requirements.txt    # Python dependencies
│   └── model.joblib        # Pre-trained XGBoost model
├── frontend/               # React Application
│   ├── src/                # UI Components & Logic
│   ├── tailwind.config.js  # Styling configuration
│   └── vite.config.js      # Build configuration
├── data/                   # Dataset & Preprocessing notebooks
├── Train.csv               # Raw training data
└── train_model.py          # ML Training script
```

---

## 📈 Model Performance
The XGBoost model was trained on supplier data, achieving high accuracy in distinguishing between punctual and delayed shipments. Key features influencing the prediction include:
- **Discount Offered**: High correlation with delivery delays.
- **Weight in gms**: Shipment weight impacts logistics mode and timing.
- **Warehouse Block**: Regional performance variations.

---

Developed with ❤️ by **Tanmay Jadhav**
