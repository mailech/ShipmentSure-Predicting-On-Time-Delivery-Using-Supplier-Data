# ShipmentSure - Predicting On-Time Delivery

## Deployment Link
https://new-shipment-prediction.vercel.app/

## Output Screenshots
![Home Page Output](screenshots/output-home.png)
![Prediction Output](screenshots/output-prediction.png)

## Target Labels
Class 1 - On time Delivery
Class 0 - Delayed Delivery
Confidence - How sure the model is about its prediction
## Insights
If confidence is:
>80% -> Strong prediction
60-80% -> Medium confidence
<60% -> Uncertain prediction

## Benefits to Use This Website
- Predicts shipment delivery status quickly using supplier and logistics inputs.
- Helps teams identify delay risks before shipment completion.
- Supports better planning for operations, inventory, and customer communication.
- Provides a simple and accessible web interface for non-technical users.
- Reduces manual analysis effort by automating prediction.

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI, Uvicorn
- Machine Learning: scikit-learn model pipeline (serialized with pickle/joblib)
- Deployment: Vercel (Frontend)
- Data Work: Jupyter Notebooks, Pandas, NumPy
