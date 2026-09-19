import streamlit as st

from src.advanced_vessel_recommendation import recommend_vessel
from src.cargo_procurement_recommendation import recommend_procurement
from src.freight_cost_optimizer import calculate_freight_cost
from src.route_risk_analysis import calculate_route_risk


st.set_page_config(
    page_title="AI Freight Decision Center",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Freight Decision Center")

st.write(
    "Integrated AI decision support for vessel chartering, "
    "bulk cargo procurement, freight cost optimization "
    "and maritime route risk analysis."
)

st.divider()

st.subheader("📋 Freight Planning Inputs")

col1, col2 = st.columns(2)

with col1:

    cargo_quantity = st.number_input(
        "📦 Cargo Quantity (MT)",
        min_value=1000,
        max_value=400000,
        value=70000,
        step=1000
    )

    distance_nm = st.number_input(
        "🌍 Route Distance (nautical miles)",
        min_value=100,
        max_value=20000,
        value=4500,
        step=100
    )

    demand_index = st.number_input(
        "📈 Freight Demand Index",
        min_value=0,
        max_value=100,
        value=85,
        step=1
    )

    procurement_price = st.number_input(
        "💰 Procurement Price (USD/MT)",
        min_value=1.0,
        max_value=1000.0,
        value=120.0,
        step=5.0
    )

with col2:

    vessel_availability = st.number_input(
        "🚢 Vessel Availability",
        min_value=1,
        max_value=40,
        value=25,
        step=1
    )

    freight_rate = st.number_input(
        "🚢 Freight Rate (USD/MT)",
        min_value=1.0,
        max_value=500.0,
        value=35.0,
        step=1.0
    )

    bunker_price = st.number_input(
        "⛽ Bunker Price (USD/ton)",
        min_value=100.0,
        max_value=1500.0,
        value=600.0,
        step=10.0
    )

    voyage_days = st.number_input(
        "🌊 Voyage Duration (days)",
        min_value=1,
        max_value=100,
        value=12,
        step=1
    )

port_waiting_hours = st.number_input(
    "⚓ Port Waiting Time (hours)",
    min_value=0,
    max_value=500,
    value=18,
    step=1
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

st.divider()

if st.button(
    "🧠 Generate Integrated AI Decision",
    use_container_width=True
):

    # -----------------------------
    # VESSEL RECOMMENDATION
    # -----------------------------

    vessel, vessel_score, utilization = recommend_vessel(
        cargo_quantity,
        distance_nm,
        vessel_availability
    )

    # -----------------------------
    # PROCUREMENT RECOMMENDATION
    # -----------------------------

    (
        procurement,
        procurement_score,
        percentage,
        recommended_quantity
    ) = recommend_procurement(
        cargo_quantity,
        demand_index,
        procurement_price,
        vessel_availability
    )

    # -----------------------------
    # FREIGHT COST CALCULATION
    # -----------------------------

    cost_result = calculate_freight_cost(
        cargo_quantity,
        freight_rate,
        bunker_price,
        voyage_days,
        port_waiting_hours,
        procurement_price
    )

    # -----------------------------
    # ROUTE RISK CALCULATION
    # -----------------------------

    risk, risk_score, estimated_delay = calculate_route_risk(
        distance_nm,
        port_congestion,
        weather_risk,
        port_waiting_hours,
        vessel_availability
    )

    # -----------------------------
    # OVERALL AI SCORE
    # -----------------------------

    overall_score = round(
        (
            vessel_score
            + procurement_score
            + (100 - risk_score)
        ) / 3,
        2
    )

    st.success("✅ AI Analysis Completed")

    # -----------------------------
    # VESSEL DECISION
    # -----------------------------

    st.subheader("🚢 Vessel Decision")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Recommended Vessel",
            vessel
        )

    with col2:
        st.metric(
            "Vessel Score",
            vessel_score
        )

    with col3:
        st.metric(
            "Vessel Utilization",
            f"{utilization:.2f}%"
        )

    # -----------------------------
    # PROCUREMENT DECISION
    # -----------------------------

    st.subheader("📦 Procurement Decision")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Procurement Action",
            procurement
        )

    with col2:
        st.metric(
            "Procurement Score",
            procurement_score
        )

    with col3:
        st.metric(
            "Recommended Quantity",
            f"{recommended_quantity:,.0f} MT"
        )

    # -----------------------------
    # FREIGHT COST ANALYSIS
    # -----------------------------

    st.divider()

    st.subheader("💰 Freight Cost Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚢 Freight Cost",
            f"${cost_result['freight_cost']:,.0f}"
        )

    with col2:
        st.metric(
            "⛽ Bunker Cost",
            f"${cost_result['bunker_cost']:,.0f}"
        )

    with col3:
        st.metric(
            "⚓ Port Waiting Cost",
            f"${cost_result['port_waiting_cost']:,.0f}"
        )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Total Logistics Cost",
            f"${cost_result['total_cost']:,.0f}"
        )

    with col2:
        st.metric(
            "📊 Cost per MT",
            f"${cost_result['cost_per_mt']:.2f}"
        )

    # -----------------------------
    # ROUTE RISK ANALYSIS
    # -----------------------------

    st.divider()

    st.subheader("🌍 Route Risk Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⚠️ Risk Level",
            risk
        )

    with col2:
        st.metric(
            "📊 Risk Score",
            f"{risk_score}/100"
        )

    with col3:
        st.metric(
            "⏳ Estimated Delay",
            f"{estimated_delay} days"
        )

    if risk == "High Risk":
        st.error(
            "⚠️ High operational risk detected. "
            "Consider reviewing the route and vessel availability."
        )

    elif risk == "Medium Risk":
        st.warning(
            "⚠️ Moderate operational risk detected. "
            "Monitor congestion and weather conditions."
        )

    else:
        st.success(
            "✅ Low operational risk detected."
        )

    # -----------------------------
    # OVERALL AI DECISION
    # -----------------------------

    st.divider()

    st.subheader("🧠 Overall AI Decision")

    st.metric(
        "Overall AI Decision Score",
        overall_score
    )

    st.info(
        f"For **{cargo_quantity:,.0f} MT** cargo over a "
        f"**{distance_nm:,.0f} nautical mile** route, the integrated "
        f"AI recommends **{vessel}** for vessel planning and "
        f"**{procurement}** for cargo procurement. "
        f"The route is classified as **{risk}** with an estimated "
        f"delay of **{estimated_delay} days**."
    )