# ShipmentSure Web App

This repository contains a complete **frontend and backend web application** for shipment delivery prediction using AI/ML models.

---

## 🚀 What Was Added

- **`backend/main.py`**: FastAPI backend API for handling predictions.  
- **`backend/requirements.txt`**: Python dependencies required to run the backend.  
- **`backend/feature_contract.json`**: Notebook-sync feature order contract for consistent model inputs.  
- **`frontend/index.html`**: Main UI page for interacting with the app.  
- **`frontend/styles.css`**: Custom Purple / neon gradient theme for the frontend.  
- **`frontend/app.js`**: Dynamic form logic and client-side code for fetching predictions.

---

## 🖥 Run Locally

From the **project root**, follow these steps:

1. Install Python dependencies:

   ```bash
   PS C:\Users\Admin\ShipmentSure-Predicting-On-Time-Delivery-Using-Supplier-Data\ -m pip install -r backend/requirements.txt

2. Run the FastAPI backend:

   ```bash
   PS C:\Users\Admin\ShipmentSure-Predicting-On-Time-Delivery-Using-Supplier-Data> uvicorn backend.main:app --reload

3.Open the app in your browser:

Frontend: http://127.0.0.1:8000
Backend API Docs: http://127.0.0.1:8000/docs


## 🎯 Features
AI-powered shipment delivery prediction
User-friendly dynamic web form
Dark and light theme support
Live confidence percentage with risk assessment
History tracking of predictions
   
## Note: 
    Make sure Python 3.11 is installed and properly configured on your system before running the app.