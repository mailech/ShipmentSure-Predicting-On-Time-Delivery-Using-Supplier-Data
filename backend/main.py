from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PIPELINE_PATH = ROOT_DIR / "models" / "model_pipeline.pkl"
BEST_MODEL_PATH = ROOT_DIR / "models" / "best_model.pkl"
TRAIN_DATA_PATH = ROOT_DIR / "data" / "Train.csv"
FRONTEND_DIR = ROOT_DIR / "frontend"
FEATURE_CONTRACT_PATH = ROOT_DIR / "backend" / "feature_contract.json"

NUMERIC_FIELDS = [
    "ID",
    "Customer_care_calls",
    "Customer_rating",
    "Cost_of_the_Product",
    "Prior_purchases",
    "Discount_offered",
    "Weight_in_gms",
]

CATEGORICAL_FIELDS = [
    "Warehouse_block",
    "Mode_of_Shipment",
    "Product_importance",
    "Gender",
]

ENGINEERED_DEFAULT_COLUMNS = [
    "ID",
    "Customer_care_calls",
    "Customer_rating",
    "Cost_of_the_Product",
    "Prior_purchases",
    "Discount_offered",
    "Weight_in_gms",
    "Warehouse_block_B",
    "Warehouse_block_C",
    "Warehouse_block_D",
    "Warehouse_block_F",
    "Mode_of_Shipment_Road",
    "Mode_of_Shipment_Ship",
    "Product_importance_low",
    "Product_importance_medium",
    "Gender_M",
]

DEFAULT_NUMERIC_STATS: Dict[str, Dict[str, int]] = {
    "ID": {"min": 1, "max": 10999, "default": 5500},
    "Customer_care_calls": {"min": 2, "max": 7, "default": 4},
    "Customer_rating": {"min": 1, "max": 5, "default": 3},
    "Cost_of_the_Product": {"min": 96, "max": 310, "default": 214},
    "Prior_purchases": {"min": 2, "max": 10, "default": 3},
    "Discount_offered": {"min": 1, "max": 65, "default": 7},
    "Weight_in_gms": {"min": 1001, "max": 7846, "default": 4149},
}

DEFAULT_CATEGORICAL_OPTIONS: Dict[str, List[str]] = {
    "Warehouse_block": ["A", "B", "C", "D", "F"],
    "Mode_of_Shipment": ["Flight", "Road", "Ship"],
    "Product_importance": ["high", "low", "medium"],
    "Gender": ["F", "M"],
}


class ShipmentRequest(BaseModel):
    ID: int = Field(..., ge=1, le=10999)
    Warehouse_block: str
    Mode_of_Shipment: str
    Customer_care_calls: int = Field(..., ge=2, le=7)
    Customer_rating: int = Field(..., ge=1, le=5)
    Cost_of_the_Product: int = Field(..., ge=96, le=310)
    Prior_purchases: int = Field(..., ge=2, le=10)
    Product_importance: str
    Gender: str
    Discount_offered: int = Field(..., ge=1, le=65)
    Weight_in_gms: int = Field(..., ge=1001, le=7846)

    @field_validator("Warehouse_block")
    @classmethod
    def validate_warehouse_block(cls, value: str) -> str:
        value = value.strip()
        if value not in DEFAULT_CATEGORICAL_OPTIONS["Warehouse_block"]:
            raise ValueError("Warehouse_block must be one of A, B, C, D, F")
        return value

    @field_validator("Mode_of_Shipment")
    @classmethod
    def validate_mode_of_shipment(cls, value: str) -> str:
        value = value.strip()
        if value not in DEFAULT_CATEGORICAL_OPTIONS["Mode_of_Shipment"]:
            raise ValueError("Mode_of_Shipment must be one of Flight, Road, Ship")
        return value

    @field_validator("Product_importance")
    @classmethod
    def validate_product_importance(cls, value: str) -> str:
        value = value.strip()
        if value not in DEFAULT_CATEGORICAL_OPTIONS["Product_importance"]:
            raise ValueError("Product_importance must be one of high, low, medium")
        return value

    @field_validator("Gender")
    @classmethod
    def validate_gender(cls, value: str) -> str:
        value = value.strip()
        if value not in DEFAULT_CATEGORICAL_OPTIONS["Gender"]:
            raise ValueError("Gender must be one of F, M")
        return value


app = FastAPI(
    title="ShipmentSure Delivery Predictor API",
    description="Backend API that serves predictions from pre-trained ShipmentSure model artifacts.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


class ModelArtifacts:
    def __init__(self) -> None:
        self.scaler = None
        self.model = None
        self.engineered_columns: List[str] = []
        self.classes: List[Any] = []


def _to_python_scalar(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    return value


def load_artifacts() -> ModelArtifacts:
    if not MODEL_PIPELINE_PATH.exists():
        raise FileNotFoundError(f"Missing model pipeline artifact: {MODEL_PIPELINE_PATH}")

    artifacts = ModelArtifacts()

    pipeline_obj = joblib.load(MODEL_PIPELINE_PATH)

    if isinstance(pipeline_obj, tuple) and len(pipeline_obj) == 2:
        artifacts.scaler, artifacts.model = pipeline_obj
    else:
        artifacts.model = pipeline_obj

    if artifacts.model is None:
        if not BEST_MODEL_PATH.exists():
            raise RuntimeError("No valid model found in model artifacts")
        artifacts.model = joblib.load(BEST_MODEL_PATH)

    if artifacts.scaler is not None and hasattr(artifacts.scaler, "feature_names_in_"):
        artifacts.engineered_columns = [str(c) for c in artifacts.scaler.feature_names_in_]
    else:
        artifacts.engineered_columns = ENGINEERED_DEFAULT_COLUMNS[:]

    if hasattr(artifacts.model, "classes_"):
        artifacts.classes = [_to_python_scalar(c) for c in artifacts.model.classes_]

    return artifacts


def _safe_int(value: Any, fallback: int) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return fallback


def _load_feature_contract(contract_path: Path) -> Dict[str, Any]:
    if not contract_path.exists():
        raise FileNotFoundError(
            f"Missing notebook feature contract: {contract_path}. "
            "Create backend/feature_contract.json to keep runtime feature order synced."
        )

    try:
        with contract_path.open("r", encoding="utf-8") as contract_file:
            contract: Dict[str, Any] = json.load(contract_file)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in feature contract: {contract_path}") from exc

    return contract


def _first_mismatch_index(expected: List[str], actual: List[str]) -> int | None:
    min_length = min(len(expected), len(actual))
    for idx in range(min_length):
        if expected[idx] != actual[idx]:
            return idx

    if len(expected) != len(actual):
        return min_length

    return None


def _validate_order_or_raise(
    *,
    expected: List[str],
    actual: List[str],
    label: str,
) -> None:
    mismatch_index = _first_mismatch_index(expected, actual)
    if mismatch_index is None:
        return

    expected_value = expected[mismatch_index] if mismatch_index < len(expected) else "<missing>"
    actual_value = actual[mismatch_index] if mismatch_index < len(actual) else "<missing>"

    missing_in_actual = [item for item in expected if item not in actual]
    extra_in_actual = [item for item in actual if item not in expected]

    raise RuntimeError(
        f"Notebook sync mismatch in {label}. "
        f"First mismatch at position {mismatch_index}: expected '{expected_value}', got '{actual_value}'. "
        f"Missing in runtime: {missing_in_actual}. Extra in runtime: {extra_in_actual}."
    )


def validate_feature_contract(
    engineered_columns: List[str],
    field_schema: List[Dict[str, Any]],
) -> Dict[str, Any]:
    contract = _load_feature_contract(FEATURE_CONTRACT_PATH)

    expected_engineered = contract.get("engineered_feature_order")
    if not isinstance(expected_engineered, list) or not expected_engineered:
        raise RuntimeError("Feature contract must include a non-empty engineered_feature_order list")
    if not all(isinstance(item, str) for item in expected_engineered):
        raise RuntimeError("engineered_feature_order must contain only strings")

    expected_raw_inputs = contract.get("raw_input_fields")
    if not isinstance(expected_raw_inputs, list) or not expected_raw_inputs:
        raise RuntimeError("Feature contract must include a non-empty raw_input_fields list")
    if not all(isinstance(item, str) for item in expected_raw_inputs):
        raise RuntimeError("raw_input_fields must contain only strings")

    runtime_raw_inputs = [str(field["name"]) for field in field_schema]

    _validate_order_or_raise(
        expected=expected_engineered,
        actual=engineered_columns,
        label="engineered feature order",
    )
    _validate_order_or_raise(
        expected=expected_raw_inputs,
        actual=runtime_raw_inputs,
        label="raw input field order",
    )

    checked_at = datetime.now(timezone.utc).isoformat()

    return {
        "sync_ok": True,
        "contract_version": str(contract.get("contract_version", "unknown")),
        "source_notebook": str(contract.get("source_notebook", "unknown")),
        "contract_path": "backend/feature_contract.json",
        "checked_at_utc": checked_at,
        "engineered_feature_count": len(engineered_columns),
        "raw_input_field_count": len(runtime_raw_inputs),
    }


def build_field_schema() -> List[Dict[str, Any]]:
    numeric_stats = {k: v.copy() for k, v in DEFAULT_NUMERIC_STATS.items()}
    category_options = {k: v[:] for k, v in DEFAULT_CATEGORICAL_OPTIONS.items()}

    if TRAIN_DATA_PATH.exists():
        try:
            df = pd.read_csv(TRAIN_DATA_PATH)
            for field in NUMERIC_FIELDS:
                if field in df.columns:
                    numeric_stats[field]["min"] = _safe_int(df[field].min(), numeric_stats[field]["min"])
                    numeric_stats[field]["max"] = _safe_int(df[field].max(), numeric_stats[field]["max"])
                    numeric_stats[field]["default"] = _safe_int(
                        df[field].median(), numeric_stats[field]["default"]
                    )
            for field in CATEGORICAL_FIELDS:
                if field in df.columns:
                    found = sorted(df[field].dropna().astype(str).unique().tolist())
                    if found:
                        category_options[field] = found
        except Exception:
            pass

    schema: List[Dict[str, Any]] = []

    for field in [
        "ID",
        "Warehouse_block",
        "Mode_of_Shipment",
        "Customer_care_calls",
        "Customer_rating",
        "Cost_of_the_Product",
        "Prior_purchases",
        "Product_importance",
        "Gender",
        "Discount_offered",
        "Weight_in_gms",
    ]:
        if field in numeric_stats:
            schema.append(
                {
                    "name": field,
                    "type": "number",
                    "min": numeric_stats[field]["min"],
                    "max": numeric_stats[field]["max"],
                    "default": numeric_stats[field]["default"],
                    "step": 1,
                }
            )
        else:
            schema.append(
                {
                    "name": field,
                    "type": "select",
                    "options": category_options[field],
                    "default": category_options[field][0],
                }
            )

    return schema


def encode_to_engineered_features(
    payload: ShipmentRequest, engineered_columns: List[str]
) -> pd.DataFrame:
    raw = payload.model_dump()

    features = {column: 0 for column in engineered_columns}

    for field in NUMERIC_FIELDS:
        if field in features:
            features[field] = int(raw[field])

    warehouse = raw["Warehouse_block"]
    for suffix in ["B", "C", "D", "F"]:
        key = f"Warehouse_block_{suffix}"
        if key in features:
            features[key] = 1 if warehouse == suffix else 0

    shipment_mode = raw["Mode_of_Shipment"]
    for suffix in ["Road", "Ship"]:
        key = f"Mode_of_Shipment_{suffix}"
        if key in features:
            features[key] = 1 if shipment_mode == suffix else 0

    importance = raw["Product_importance"]
    for suffix in ["low", "medium"]:
        key = f"Product_importance_{suffix}"
        if key in features:
            features[key] = 1 if importance == suffix else 0

    if "Gender_M" in features:
        features["Gender_M"] = 1 if raw["Gender"] == "M" else 0

    encoded_df = pd.DataFrame(
        [[features[col] for col in engineered_columns]],
        columns=engineered_columns,
    )
    return encoded_df


ARTIFACTS = load_artifacts()
FIELD_SCHEMA = build_field_schema()
NOTEBOOK_SYNC_STATUS = validate_feature_contract(ARTIFACTS.engineered_columns, FIELD_SCHEMA)


@app.get("/", include_in_schema=False)
def serve_frontend() -> FileResponse:
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend index.html was not found")
    return FileResponse(index_path)


@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    return {
        "status": "ok",
        "project": "ShipmentSure",
        "model_locked": True,
        "artifact": "models/model_pipeline.pkl",
        "engineered_feature_count": len(ARTIFACTS.engineered_columns),
        "classes": ARTIFACTS.classes,
        "notebook_sync": NOTEBOOK_SYNC_STATUS,
    }


@app.get("/api/schema")
def get_schema() -> Dict[str, Any]:
    return {
        "project": "ShipmentSure",
        "target": "Reached.on.Time_Y.N",
        "model_locked": True,
        "raw_fields": FIELD_SCHEMA,
        "engineered_features": ARTIFACTS.engineered_columns,
        "classes": ARTIFACTS.classes,
        "notebook_sync": NOTEBOOK_SYNC_STATUS,
        "notes": [
            "Artifacts are loaded read-only; no retraining is performed.",
            "Prediction output is the raw target class label from the trained model.",
            "Feature order and raw input mapping are validated against backend/feature_contract.json at startup.",
        ],
    }


@app.post("/api/predict")
def predict(payload: ShipmentRequest) -> Dict[str, Any]:
    try:
        model_input_df = encode_to_engineered_features(payload, ARTIFACTS.engineered_columns)

        transformed = model_input_df
        if ARTIFACTS.scaler is not None:
            transformed = ARTIFACTS.scaler.transform(model_input_df)

        raw_prediction = ARTIFACTS.model.predict(transformed)[0]
        prediction = _to_python_scalar(raw_prediction)

        class_probabilities: Dict[str, float] = {}
        confidence = 1.0

        if hasattr(ARTIFACTS.model, "predict_proba"):
            proba_values = ARTIFACTS.model.predict_proba(transformed)[0]
            for cls, prob in zip(ARTIFACTS.classes, proba_values):
                class_probabilities[str(cls)] = round(float(prob), 6)
            if class_probabilities:
                confidence = max(class_probabilities.values())

        return {
            "prediction": prediction,
            "prediction_label": f"Target class {prediction}",
            "confidence": round(float(confidence), 6),
            "class_probabilities": class_probabilities,
            "model_locked": True,
            "message": "Prediction created with the existing trained model artifacts.",
            "target_hint": "Interpret class labels based on your notebook target mapping.",
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
