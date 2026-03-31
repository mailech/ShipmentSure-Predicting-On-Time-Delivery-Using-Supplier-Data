# ShipmentSure Web App

This repository now includes a complete frontend and backend web application for model inference.

## What Was Added

- `backend/main.py`: FastAPI backend API
- `backend/requirements.txt`: Python dependencies for the web app
- `backend/feature_contract.json`: Notebook-sync feature order contract
- `frontend/index.html`: Main UI page
- `frontend/styles.css`: Custom red-themed design
- `frontend/app.js`: Dynamic form + prediction client logic

## Model Safety

The app only **loads and uses** existing artifacts:

- `models/model_pipeline.pkl`
- `models/best_model.pkl`

No retraining, rewriting, or mutation of model files is performed.

## Run Locally

From the project root:

```powershell
C:/Users/KIIT0001/AppData/Local/Microsoft/WindowsApps/python3.11.exe -m pip install -r backend/requirements.txt
C:/Users/KIIT0001/AppData/Local/Microsoft/WindowsApps/python3.11.exe -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- `http://127.0.0.1:8000` for the frontend
- `http://127.0.0.1:8000/docs` for backend API docs

## API Endpoints

- `GET /api/health`: Backend/model health details
- `GET /api/schema`: Input schema and model metadata
- `POST /api/predict`: Single prediction endpoint

## Notebook Sync Validation

At startup, the backend validates:

- raw input field order
- engineered feature order

against `backend/feature_contract.json`.

If contract and runtime model features do not match, startup fails fast with an explicit mismatch error.

## Notes on Target Labels

Predictions return the raw trained target class (`0` or `1`) from `Reached.on.Time_Y.N`.
Interpret business meaning of label values according to your notebook conventions.
