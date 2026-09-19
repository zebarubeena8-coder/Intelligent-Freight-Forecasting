import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="AI Freight Forecasting",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 AI Freight Demand Forecasting")

st.write(
    "AI-powered freight demand prediction for overseas bulk cargo "
    "movement to East Coast Indian ports."
)

st.divider()

# -----------------------------
# LOAD MODEL
# -----------------------------

@st.cache_resource
def load_model():
    return joblib.load(
        "models/maritime_forecasting_model.pkl"
    )


model = load_model()

# -----------------------------
# INPUTS
# -----------------------------

st.subheader("📋 Voyage Parameters")

col1, col2 = st.columns(2)

with col1:

    cargo_quantity = st.number_input(
        "📦 Cargo Quantity (MT)",
        min_value=10000.0,
        max_value=400000.0,
        value=70000.0,
        step=1000.0
    )

    vessel_capacity = st.number_input(
        "🚢 Vessel Capacity (MT)",
        min_value=10000.0,
        max_value=400000.0,
        value=70000.0,
        step=1000.0
    )

    distance_nm = st.number_input(
        "🌍 Route Distance (nautical miles)",
        min_value=100.0,
        max_value=20000.0,
        value=4500.0,
        step=100.0
    )

    voyage_days = st.number_input(
        "🌊 Voyage Duration (days)",
        min_value=1.0,
        max_value=100.0,
        value=12.0,
        step=1.0
    )

    bunker_price = st.number_input(
        "⛽ Bunker Price (USD/ton)",
        min_value=100.0,
        max_value=1500.0,
        value=600.0,
        step=10.0
    )

with col2:

    port_congestion = st.number_input(
        "⚓ Port Congestion",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.1
    )

    weather_risk = st.number_input(
        "🌦️ Weather Risk",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1
    )

    port_waiting_hours = st.number_input(
        "⏱️ Port Waiting Time (hours)",
        min_value=0.0,
        max_value=500.0,
        value=18.0,
        step=1.0
    )

    vessel_availability = st.number_input(
        "🚢 Vessel Availability",
        min_value=1.0,
        max_value=40.0,
        value=25.0,
        step=1.0
    )

    procurement_price = st.number_input(
        "💰 Procurement Price (USD/MT)",
        min_value=1.0,
        max_value=1000.0,
        value=120.0,
        step=5.0
    )

    freight_rate = st.number_input(
        "🚢 Freight Rate (USD/MT)",
        min_value=1.0,
        max_value=500.0,
        value=35.0,
        step=1.0
    )

st.divider()

# -----------------------------
# PREDICTION
# -----------------------------

if st.button(
    "🔮 Predict Freight Demand",
    use_container_width=True
):

    input_data = pd.DataFrame([{
        "cargo_quantity_mt": cargo_quantity,
        "vessel_capacity_mt": vessel_capacity,
        "distance_nm": distance_nm,
        "voyage_days": voyage_days,
        "bunker_price_usd_ton": bunker_price,
        "port_congestion": port_congestion,
        "weather_risk": weather_risk,
        "port_waiting_hours": port_waiting_hours,
        "vessel_availability": vessel_availability,
        "procurement_price_usd_mt": procurement_price,
        "freight_rate_usd_mt": freight_rate,
        "charter_cost_usd": cargo_quantity * freight_rate
    }])

    prediction = model.predict(input_data)[0]

    prediction = max(0, prediction)

    st.success("✅ Freight Demand Prediction Completed")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📈 Predicted Freight Demand",
            f"{prediction:,.2f}"
        )

    with col2:
        st.metric(
            "💰 Estimated Charter Cost",
            f"${cargo_quantity * freight_rate:,.0f}"
        )

    st.divider()

    if prediction >= 80:
        st.success(
            "🔥 High freight demand detected. "
            "Consider securing vessel capacity and cargo supply early."
        )

    elif prediction >= 50:
        st.warning(
            "⚠️ Moderate freight demand detected. "
            "Monitor market conditions before finalizing procurement."
        )

    else:
        st.info(
            "📉 Lower freight demand detected. "
            "Market monitoring may be appropriate."
        )