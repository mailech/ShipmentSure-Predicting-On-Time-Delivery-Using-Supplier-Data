# ShipmentSure AI - Architecture & Flow Report

This document serves as a comprehensive presentation guide for the **ShipmentSure AI** project. It explains the "Why", "What", and "How" behind the full-stack architecture, enabling an in-depth understanding of the system's inner workings.

---

## 1. System Overview & Architecture
ShipmentSure AI is an end-to-end Machine Learning web application designed to predict the reliability of e-commerce and supply chain deliveries. It features a bold **Neobrutalism UI** (Frontend), a lightweight REST API (Backend), and an **XGBoost machine learning pipeline** (Model).

**The Tech Stack:**
- **Model Engine:** Scikit-Learn + XGBoost (Calibrated)
- **Training Strategy:** 80/20 Train-Test Split with CV Calibration

---

## 2. The Inputs: Why Are These Fields Required?
The user interface requests exactly 8 inputs. These match precisely with the data the ML model expects. Each input plays a vital role in determining if a package will arrive on time or be delayed:

1. **Warehouse Block (A, B, C, D, F):** Analyzes if certain company warehouses suffer from deeper logistical bottlenecks.
2. **Mode of Shipment (Flight, Ship, Road):** Flight is usually faster but weather-dependent, whereas Ships are slower. The model weighs this heavily against the "Weight" column.
3. **Product Importance (Low, Medium, High):** High-importance products are often prioritized by couriers.
4. **Customer Care Calls:** High numbers of calls usually indicate the customer is already facing issues or the package is difficult to track.
5. **Customer Rating (1-5):** A historical metric of customer satisfaction, which might correlate with specific delivery regions or product types.
6. **Prior Purchases:** Loyal customers might get priority shipping from the business side.
7. **Discount Offered (%):** Highly discounted products might be shipped via cheaper, slower economy shipping routes.
8. **Weight (g):** Heavy packages are harder to move quickly and might be restricted from air travel.

---

## 3. The Process: Step-by-Step Flow

When a user clicks **"PREDICT DELIVERY RELIABILITY"**, an entire cascade of events happens across three layers.

### Phase A: The React Frontend (The Trigger)
1. **State Collection:** The `InputForm.jsx` component wraps all user inputs into a single JSON object. 
2. **API Call (`services/api.js`):** React uses `axios` to send this JSON object as an HTTP POST request to `http://localhost:5000/api/predict`.
3. **Wait State:** React disables the button and sets `isLoading = true` while waiting for the server.

### Phase B: The Flask Backend (The Brain)
*(Located in `backend/app.py`)*

1. **Endpoint Triggered:** The `@app.route('/api/predict', methods=['POST'])` catches the incoming request.
2. **Validation:** The server checks `if field not in data`. If the frontend forgot to send the "Weight", the backend immediately rejects it with a `400 Bad Request` to prevent a server crash.
3. **Data Type Conversion:** Input data coming from the web is natively mapped as strings/objects. Flask manually converts numerical strings into integers (e.g., `int(data['Weight_in_gms'])`).
4. **Pandas DataFrame:** The dictionary is wrapped into a 2D array known as a DataFrame (`df = pd.DataFrame([data])`). The ML model only understands DataFrames.
5. **Prediction:** `prob = float(model.predict_proba(df)[0][1])`
   - `model` is our pre-trained XGBoost Pipeline.
   - `predict_proba` returns an array of two percentages: `[Chance_of_Delay, Chance_of_On_Time]`.
   - `[0][1]` grabs the probability of being "On Time".
   - `float()` ensures the Numpy datatype is converted to a native Python float so it can be sent back to the browser.
6. **Enrichment:** Flask calculates the `confidence` margin and a `risk_level` (High/Medium/Low) based on the pure probability score.
7. **Return:** Flask bundles this enriched data into a JSON response.

### Phase C: Preprocessing & Calibration Magic
*(Built via `train_model.py`)*

When Flask calls `predict_proba`, the data passes through a multi-stage **Calibrated Pipeline**:
1. **OneHotEncoder:** Converts words (like "Flight") into binary math columns.
2. **StandardScaler:** Normalizes numbers like "Weight" so they don't over-influence the trees.
3. **XGBoost Inference:** Uses optimized trees (`max_depth=4`, `learning_rate=0.05`) to prevent overfitting.
4. **Sigmoid Calibration (`CalibratedClassifierCV`):** Smooths the raw XGBoost scores into "Calibrated Probabilities," ensuring the model isn't "overconfident" (avoiding 100% or 0% results).
5. **Class Balancing (`scale_pos_weight`):** Since the dataset has more "Delayed" cases (60%) than "On-Time" cases (40%), the model could naturally bias towards predicting delays. I handled this by adjusting class weights using `scale_pos_weight=0.68` to balance the model's perception and ensure fairer predictions for reliable shipments.

**Current Performance:** The model currently achieves an accuracy of **~66%** on unseen test data—a solid benchmark for this supply chain dataset.

---

## 4. The Outputs: Rendering the Results
The frontend receives the prediction and updates the UI instantly:

1. **Animated Counter (`PredictionCard.jsx`):** A `setInterval` loop physically counts up from `0%` to the received `87%` probability. This gives the app a dynamic, "analyzing" feel.
2. **Status Colors:** An `if/else` statement checks the `risk_level`. 
   - Safety (Low Risk): Green `ShieldCheck` icon.
   - Risk: Yellow `ShieldAlert`.
   - Delayed: Red `ShieldAlert`.
3. **Local Storage (`PredictionHistory.jsx`):** The prediction is saved in browser cache (`localStorage.setItem()`). If the user refreshes the page, their historical predictions stay alive in the table. 

---

## 5. Real-World Applications & Business Value

When presenting this project, it is essential to highlight *why* this matters. This is not just a math project; it generates actual business ROI:

* **Proactive Customer Support:** If the ML model flags a high-priority customer's package as "Delayed" (Red Status), a company can instantly trigger an apologetic email or offer a partial refund *before* the customer even complains.
* **Dynamic Shipping Automation:** If the model predicts an unacceptably high risk of delay from Warehouse F using 'Road' transport, the company's routing software can dynamically upgrade the package to 'Flight' transportation.
* **Supply Chain Audits:** By analyzing *Feature Importance*, stakeholders can accurately identify which carrier or which warehouse is currently forming the biggest bottleneck in their network.
