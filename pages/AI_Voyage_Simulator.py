import streamlit as st
from src.advanced_vessel_recommendation import recommend_vessel
from src.cargo_procurement_recommendation import recommend_procurement
from src.freight_cost_optimizer import calculate_freight_cost
from src.route_risk_analysis import calculate_route_risk


st.set_page_config(
    page_title="AI Voyage Simulator",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 AI Voyage Scenario Simulator")

st.write(
    "Simulate an overseas bulk-cargo voyage and evaluate "
    "vessel selection, procurement, logistics cost and route risk."
)

st.divider()

st.subheader("📋 Scenario Inputs")

col1, col2 = st.columns(2)

with col1:

    cargo_quantity = st.number_input(
        "📦 Cargo Quantity (MT)",
        min_value=10000,
        max_value=400000,
        value=70000,
        step=5000
    )

    distance_nm = st.number_input(
        "🌍 Voyage Distance (NM)",
        min_value=100,
        max_value=20000,
        value=4500,
        step=100
    )

    demand_index = st.slider(
        "📈 Freight Demand Index",
        0,
        100,
        85
    )

    procurement_price = st.number_input(
        "💰 Procurement Price (USD/MT)",
        min_value=1.0,
        max_value=1000.0,
        value=120.0,
        step=5.0
    )

with col2:

    vessel_availability = st.slider(
        "🚢 Vessel Availability",
        1,
        40,
        25
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

port_congestion = st.slider(
    "⚓ Port Congestion",
    0.0,
    1.0,
    0.4,
    0.1
)

weather_risk = st.slider(
    "🌦️ Weather Risk",
    0.0,
    1.0,
    0.3,
    0.1
)

port_waiting_hours = st.number_input(
    "⏱️ Port Waiting Time (hours)",
    min_value=0,
    max_value=500,
    value=18,
    step=1
)

st.divider()

if st.button(
    "🚀 Run AI Voyage Simulation",
    use_container_width=True
):

    # Vessel AI
    vessel, vessel_score, utilization = recommend_vessel(
        cargo_quantity,
        distance_nm,
        vessel_availability
    )

    # Procurement AI
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

    # Cost AI
    cost = calculate_freight_cost(
        cargo_quantity,
        freight_rate,
        bunker_price,
        voyage_days,
        port_waiting_hours,
        procurement_price
    )

    # Risk AI
    risk, risk_score, estimated_delay = calculate_route_risk(
        distance_nm,
        port_congestion,
        weather_risk,
        port_waiting_hours,
        vessel_availability
    )

    # Overall score
    overall_score = round(
        (
            vessel_score
            + procurement_score
            + (100 - risk_score)
        ) / 3,
        2
    )

    st.success("✅ Voyage Simulation Completed")

    # -----------------------------
    # KEY RESULTS
    # -----------------------------

    st.subheader("🎯 Simulation Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🚢 Vessel",
            vessel
        )

    with col2:
        st.metric(
            "📦 Procurement",
            procurement
        )

    with col3:
        st.metric(
            "⚠️ Route Risk",
            risk
        )

    with col4:
        st.metric(
            "🧠 AI Score",
            overall_score
        )

    st.divider()

    # -----------------------------
    # VESSEL
    # -----------------------------

    st.subheader("🚢 Vessel Recommendation")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Vessel Type",
            vessel
        )

    with col2:
        st.metric(
            "Utilization",
            f"{utilization:.2f}%"
        )

    # -----------------------------
    # PROCUREMENT
    # -----------------------------

    st.subheader("📦 Procurement Recommendation")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Action",
            procurement
        )

    with col2:
        st.metric(
            "Procurement %",
            f"{percentage}%"
        )

    with col3:
        st.metric(
            "Recommended Quantity",
            f"{recommended_quantity:,.0f} MT"
        )

    # -----------------------------
    # COST
    # -----------------------------

    st.subheader("💰 Logistics Cost")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Freight Cost",
            f"${cost['freight_cost']:,.0f}"
        )

    with col2:
        st.metric(
            "Bunker Cost",
            f"${cost['bunker_cost']:,.0f}"
        )

    with col3:
        st.metric(
            "Port Waiting Cost",
            f"${cost['port_waiting_cost']:,.0f}"
        )

    st.metric(
        "Total Logistics Cost",
        f"${cost['total_cost']:,.0f}"
    )

    # -----------------------------
    # RISK
    # -----------------------------

    st.subheader("🌍 Route Risk")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Risk Level",
            risk
        )

    with col2:
        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )

    with col3:
        st.metric(
            "Estimated Delay",
            f"{estimated_delay} days"
        )

    # -----------------------------
    # FINAL AI SUMMARY
    # -----------------------------

    st.divider()

    st.subheader("🧠 AI Scenario Summary")

    st.info(
        f"For a **{cargo_quantity:,.0f} MT** voyage covering "
        f"**{distance_nm:,.0f} NM**, the simulator identifies "
        f"**{vessel}** as the vessel recommendation, "
        f"**{procurement}** as the procurement action, and "
        f"**{risk}** as the route-risk level. "
        f"The estimated logistics cost is "
        f"**${cost['total_cost']:,.0f}** with an estimated delay "
        f"of **{estimated_delay} days**."
    )