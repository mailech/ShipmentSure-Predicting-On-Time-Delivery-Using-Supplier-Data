import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.calibration import CalibratedClassifierCV
from xgboost import XGBClassifier
import joblib

def train_and_save_model():
    print("📦 Loading data...")
    df = pd.read_csv("Train.csv")

    # Features
    categorical_features = ['Warehouse_block', 'Mode_of_Shipment', 'Product_importance']
    numeric_features = [
        'Customer_care_calls', 'Customer_rating',
        'Prior_purchases', 'Discount_offered', 'Weight_in_gms'
    ]

    X = df[numeric_features + categorical_features]
    y = df['Reached.on.Time_Y.N']

    print("\n📊 Target Distribution:")
    print(y.value_counts(normalize=True))

    # ✅ Stratified Split (IMPORTANT)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("\n⚙️ Building preprocessing pipeline...")

    # Preprocessing
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    # ✅ PRODUCTION-READY XGBoost Model (Hyperparameter Tuning)
    # Define parameter grid for optimization
    param_grid = {
        'model__n_estimators': [100, 200, 300],
        'model__max_depth': [3, 4, 5, 6],
        'model__learning_rate': [0.01, 0.05, 0.1, 0.2],
        'model__subsample': [0.6, 0.8, 1.0],
        'model__colsample_bytree': [0.6, 0.8, 1.0],
        'model__reg_alpha': [0, 0.1, 0.5, 1.0],
        'model__reg_lambda': [0.1, 1.0, 5.0]
    }

    base_xgboost = XGBClassifier(
        scale_pos_weight=0.68,   # Balances 60% Delay vs 40% On-Time
        random_state=42,
        eval_metric='logloss',
        n_jobs=-1
    )

    # Pipeline
    base_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', base_xgboost)
    ])

    print("\n🧠 Running Hyperparameter Optimization (this may take a moment)...")
    
    random_search = RandomizedSearchCV(
        estimator=base_pipeline,
        param_distributions=param_grid,
        n_iter=10,
        scoring='accuracy',
        cv=3,
        random_state=42,
        n_jobs=-1
    )
    
    random_search.fit(X_train, y_train)
    print(f"✅ Best CV Accuracy: {random_search.best_score_:.4f}")
    
    # Use the best model found for calibration
    best_pipeline = random_search.best_estimator_

    print("\n🧠 Training calibrated model on optimal parameters...")

    # ✅ Calibration
    calibrated_model = CalibratedClassifierCV(
        estimator=best_pipeline,
        method='sigmoid',
        cv=5
    )

    calibrated_model.fit(X_train, y_train)

    print("\n📈 Evaluating model...")

    y_pred = calibrated_model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✅ Accuracy: {accuracy:.4f}")

    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))

    # Check probabilities
    print("\n🔍 Sample Probabilities:")
    probs = calibrated_model.predict_proba(X_test[:5])
    print(probs)

    print("\n💾 Saving model as model.joblib...")
    joblib.dump(calibrated_model, "model.joblib")

    print("🎉 Done! Model is ready for backend use.")

if __name__ == "__main__":
    train_and_save_model()