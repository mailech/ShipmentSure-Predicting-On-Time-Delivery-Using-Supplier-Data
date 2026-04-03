import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="ShipmentSure",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- PREMIUM UI CSS ----------
st.markdown("""
<style>
/* ===== GLOBAL ===== */
.stApp {
    background: linear-gradient(135deg, #0b1020 0%, #111827 50%, #0f172a 100%);
    color: #f8fafc;
    animation: fadeInPage 0.8s ease-in-out;
}

@keyframes fadeInPage {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* DO NOT HIDE HEADER - sidebar arrow is there */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1450px;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: rgba(8, 15, 30, 0.96);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 18px;
    letter-spacing: 0.3px;
}

/* ===== INPUTS ===== */
label, .stNumberInput label, .stSelectbox label {
    color: #e5e7eb !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #111827 !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    min-height: 45px !important;
}

input {
    color: white !important;
    font-size: 15px !important;
}

/* ===== BUTTON ===== */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    padding: 10px 18px;
    transition: all 0.3s ease;
    box-shadow: 0 8px 18px rgba(37,99,235,0.20);
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #4338ca);
    transform: translateY(-2px);
    color: white;
}

/* ===== HERO ===== */
.hero {
    background: linear-gradient(135deg, rgba(37,99,235,0.95), rgba(79,70,229,0.92));
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 12px 30px rgba(37,99,235,0.25);
    margin-bottom: 24px;
    animation: slideDown 0.7s ease;
}

@keyframes slideDown {
    from {transform: translateY(-20px); opacity: 0;}
    to {transform: translateY(0); opacity: 1;}
}

.hero-small {
    font-size: 14px;
    font-weight: 700;
    color: #dbeafe;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

.hero-title {
    font-size: 54px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 8px;
}

.hero-sub {
    font-size: 20px;
    font-weight: 600;
    color: #eff6ff;
    margin-bottom: 10px;
}

.hero-desc {
    font-size: 15px;
    color: #dbeafe;
    line-height: 1.7;
    max-width: 900px;
}

/* ===== KPI CARDS ===== */
.kpi-card {
    background: rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    min-height: 120px;
    animation: fadeUp 0.8s ease;
}

@keyframes fadeUp {
    from {transform: translateY(20px); opacity: 0;}
    to {transform: translateY(0); opacity: 1;}
}

.kpi-title {
    font-size: 14px;
    color: #cbd5e1;
    font-weight: 700;
    margin-bottom: 10px;
}

.kpi-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.kpi-icon {
    font-size: 24px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
}

.success-text {
    color: #4ade80;
}

.delay-text {
    color: #fb7185;
}

/* ===== SECTION CARDS ===== */
.section-card {
    background: rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 22px;
    margin-top: 18px;
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    animation: fadeUp 0.9s ease;
}

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 6px;
}

.section-sub {
    font-size: 14px;
    color: #cbd5e1;
    margin-bottom: 16px;
}

.summary-item {
    font-size: 15px;
    color: #e2e8f0;
    margin-bottom: 10px;
    line-height: 1.6;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #2563eb, #60a5fa);
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown('<div class="sidebar-title">Shipment Input</div>', unsafe_allow_html=True)

warehouse_block = st.sidebar.selectbox(
    "Warehouse Block",
    ["A", "B", "C", "D", "F"],
    key="warehouse_block"
)

mode_of_shipment = st.sidebar.selectbox(
    "Mode of Shipment",
    ["Ship", "Flight", "Road"],
    key="mode_of_shipment"
)

customer_care_calls = st.sidebar.number_input(
    "Customer Care Calls",
    min_value=0,
    value=4,
    step=1,
    key="customer_care_calls"
)

customer_rating = st.sidebar.number_input(
    "Customer Rating",
    min_value=1,
    max_value=5,
    value=3,
    step=1,
    key="customer_rating"
)

cost_of_product = st.sidebar.number_input(
    "Cost of Product",
    min_value=0.0,
    value=250.0,
    step=1.0,
    key="cost_of_product"
)

prior_purchases = st.sidebar.number_input(
    "Prior Purchases",
    min_value=0,
    value=3,
    step=1,
    key="prior_purchases"
)

product_importance = st.sidebar.selectbox(
    "Product Importance",
    ["low", "medium", "high"],
    key="product_importance"
)

gender = st.sidebar.selectbox(
    "Gender",
    ["M", "F"],
    key="gender"
)

discount_offered = st.sidebar.number_input(
    "Discount Offered",
    min_value=0.0,
    value=10.0,
    step=1.0,
    key="discount_offered"
)

weight_in_gms = st.sidebar.number_input(
    "Weight in gms",
    min_value=0.0,
    value=3000.0,
    step=1.0,
    key="weight_in_gms"
)

predict_btn = st.sidebar.button("Generate Prediction", key="predict_btn")

# ---------- PREDICTION LOGIC ----------
def predict_delivery(calls, rating, cost, prior, discount, weight, mode, importance):
    score = 0

    if calls <= 3:
        score += 15
    else:
        score -= 10

    if rating >= 4:
        score += 20
    else:
        score -= 5

    if prior >= 3:
        score += 10

    if discount > 20:
        score -= 10

    if weight < 2500:
        score += 15
    else:
        score -= 8

    if mode == "Flight":
        score += 20
    elif mode == "Road":
        score += 5
    else:
        score += 10

    if importance == "high":
        score += 12
    elif importance == "medium":
        score += 6

    confidence = min(max(score + 50, 5), 95)

    if confidence >= 60:
        return "On-Time Delivery", confidence
    return "Delayed Delivery", confidence

prediction, confidence = predict_delivery(
    customer_care_calls,
    customer_rating,
    cost_of_product,
    prior_purchases,
    discount_offered,
    weight_in_gms,
    mode_of_shipment,
    product_importance
)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="hero-small">SMART LOGISTICS DASHBOARD</div>
    <div class="hero-title">ShipmentSure</div>
    <div class="hero-sub">Predicting On-Time Delivery Using Supplier Data</div>
    <div class="hero-desc">
        A premium shipment analytics dashboard that estimates whether a delivery will be on time or delayed using supplier and shipment-related inputs.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- KPI CARDS ----------
k1, k2, k3, k4 = st.columns(4)

with k1:
    status = "On-Time" if prediction == "On-Time Delivery" else "Delayed"
    color_class = "success-text" if prediction == "On-Time Delivery" else "delay-text"
    icon = "✅" if prediction == "On-Time Delivery" else "⚠️"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Delivery Status</div>
        <div class="kpi-row">
            <span class="kpi-icon">{icon}</span>
            <span class="kpi-value {color_class}">{status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Confidence Score</div>
        <div class="kpi-row">
            <span class="kpi-icon">📊</span>
            <span class="kpi-value">{confidence}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    mode_icon = "✈️" if mode_of_shipment == "Flight" else ("🚚" if mode_of_shipment == "Road" else "🚢")
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Shipment Mode</div>
        <div class="kpi-row">
            <span class="kpi-icon">{mode_icon}</span>
            <span class="kpi-value" style="font-size:22px;">{mode_of_shipment}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Warehouse</div>
        <div class="kpi-row">
            <span class="kpi-icon">🏭</span>
            <span class="kpi-value" style="font-size:22px;">{warehouse_block}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- MAIN CONTENT ----------
left, right = st.columns([1.25, 1])

with left:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">Dashboard Graph</div>
        <div class="section-sub">Visual comparison of key shipment indicators</div>
    """, unsafe_allow_html=True)

    graph_df = pd.DataFrame({
        "Metric": ["Confidence", "Customer Rating x20", "Prior Purchases x10", "Discount"],
        "Value": [confidence, customer_rating * 20, prior_purchases * 10, discount_offered]
    })

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(graph_df["Metric"], graph_df["Value"])
    ax.set_ylabel("Value")
    ax.set_ylim(0, 100)
    ax.set_title("Shipment Performance Indicators")
    st.pyplot(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">Prediction Overview</div>
        <div class="section-sub">Current delivery decision summary</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="summary-item"><b>Delivery Outcome:</b> {prediction}</div>
    <div class="summary-item"><b>Confidence Score:</b> {confidence}%</div>
    <div class="summary-item"><b>Shipment Mode:</b> {mode_of_shipment}</div>
    <div class="summary-item"><b>Warehouse Block:</b> {warehouse_block}</div>
    <div class="summary-item"><b>Customer Rating:</b> {customer_rating}</div>
    """, unsafe_allow_html=True)

    st.progress(confidence / 100)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SUMMARY ----------
st.markdown("""
<div class="section-card">
    <div class="section-title">Shipment Summary</div>
    <div class="section-sub">Current selected shipment details</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="summary-item"><b>Warehouse Block:</b> {warehouse_block}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-item"><b>Mode of Shipment:</b> {mode_of_shipment}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-item"><b>Customer Care Calls:</b> {customer_care_calls}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-item"><b>Customer Rating:</b> {customer_rating}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-item"><b>Cost of Product:</b> {cost_of_product}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-item"><b>Prior Purchases:</b> {prior_purchases}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-item"><b>Product Importance:</b> {product_importance}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-item"><b>Gender:</b> {gender}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-item"><b>Discount Offered:</b> {discount_offered}%</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-item"><b>Weight in gms:</b> {weight_in_gms}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

if predict_btn:
    st.success("Prediction generated successfully.")