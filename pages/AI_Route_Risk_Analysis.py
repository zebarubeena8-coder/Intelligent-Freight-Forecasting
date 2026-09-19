import streamlit as st
from src.route_risk_analysis import calculate_route_risk

st.set_page_config(
    page_title="AI Route Risk Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 AI Route Risk Analysis")
st.write(
    "Analyze maritime route risk using distance, "
    "port congestion, weather and vessel availability."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    distance_nm = st.number_input(
        "🌍 Route Distance (nautical miles)",
        min_value=100,
        max_value=20000,
        value=4500,
        step=100
    )

    port_congestion = st.number_input(
        "⚓ Port Congestion (0–1)",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.1
    )

    weather_risk = st.number_input(
        "🌦️ Weather Risk (0–1)",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1
    )

with col2:
    port_waiting_hours = st.number_input(
        "⏱️ Port Waiting Time (hours)",
        min_value=0,
        max_value=500,
        value=18,
        step=1
    )

    vessel_availability = st.number_input(
        "🚢 Vessel Availability",
        min_value=1,
        max_value=40,
        value=25,
        step=1
    )

st.divider()

if st.button(
    "🌍 Analyze Route Risk",
    use_container_width=True
):

    risk, score, delay = calculate_route_risk(
        distance_nm,
        port_congestion,
        weather_risk,
        port_waiting_hours,
        vessel_availability
    )

    st.success("✅ Route Analysis Completed")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⚠️ Risk Level",
            risk
        )

    with col2:
        st.metric(
            "📊 Risk Score",
            f"{score}/100"
        )

    with col3:
        st.metric(
            "⏳ Estimated Delay",
            f"{delay} days"
        )

    if risk == "High Risk":
        st.error("⚠️ High operational risk detected.")

    elif risk == "Medium Risk":
        st.warning("⚠️ Moderate operational risk detected.")

    else:
        st.success("✅ Low operational risk detected.")