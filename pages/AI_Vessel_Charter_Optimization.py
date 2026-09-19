import streamlit as st
import pandas as pd

from src.advanced_vessel_recommendation import recommend_vessel
from src.freight_cost_optimizer import calculate_freight_cost


st.set_page_config(
    page_title="AI Vessel Charter Optimization",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 AI Vessel Charter Optimization")

st.write(
    "AI-powered vessel selection and charter planning for "
    "bulk cargo transportation from overseas to East Coast India."
)

st.divider()

# -----------------------------
# INPUTS
# -----------------------------

st.subheader("📋 Charter Planning Inputs")

col1, col2 = st.columns(2)

with col1:

    cargo_quantity = st.number_input(
        "📦 Cargo Quantity (MT)",
        min_value=10000,
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

    freight_rate = st.number_input(
        "💰 Freight Rate (USD/MT)",
        min_value=1.0,
        max_value=500.0,
        value=35.0,
        step=1.0
    )

with col2:

    vessel_availability = st.number_input(
        "🚢 Vessel Availability",
        min_value=1,
        max_value=40,
        value=25,
        step=1
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

procurement_price = st.number_input(
    "📦 Procurement Price (USD/MT)",
    min_value=1.0,
    max_value=1000.0,
    value=120.0,
    step=5.0
)

st.divider()

# -----------------------------
# AI VESSEL OPTIMIZATION
# -----------------------------

if st.button(
    "🚢 Optimize Vessel Charter",
    use_container_width=True
):

    vessel, vessel_score, utilization = recommend_vessel(
        cargo_quantity,
        distance_nm,
        vessel_availability
    )

    cost = calculate_freight_cost(
        cargo_quantity,
        freight_rate,
        bunker_price,
        voyage_days,
        port_waiting_hours,
        procurement_price
    )

    st.success("✅ Vessel Charter Optimization Completed")

    # -----------------------------
    # MAIN RESULT
    # -----------------------------

    st.subheader("🎯 AI Charter Recommendation")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚢 Recommended Vessel",
            vessel
        )

    with col2:
        st.metric(
            "📊 Vessel Score",
            vessel_score
        )

    with col3:
        st.metric(
            "📦 Vessel Utilization",
            f"{utilization:.2f}%"
        )

    st.divider()

    # -----------------------------
    # COST ANALYSIS
    # -----------------------------

    st.subheader("💰 Charter Cost Analysis")

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

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Logistics Cost",
            f"${cost['total_cost']:,.0f}"
        )

    with col2:
        st.metric(
            "Logistics Cost per MT",
            f"${cost['cost_per_mt']:.2f}"
        )

    st.divider()

    # -----------------------------
    # CHART
    # -----------------------------

    st.subheader("📊 Charter Cost Breakdown")

    chart_data = pd.DataFrame({
        "Cost Component": [
            "Freight",
            "Bunker",
            "Port Waiting",
            "Procurement"
        ],
        "Cost (USD)": [
            cost["freight_cost"],
            cost["bunker_cost"],
            cost["port_waiting_cost"],
            cost["procurement_cost"]
        ]
    })

    st.bar_chart(
        chart_data.set_index("Cost Component")
    )

    st.divider()

    # -----------------------------
    # AI EXPLANATION
    # -----------------------------

    st.subheader("🤖 AI Charter Explanation")

    if utilization >= 90:
        utilization_message = (
            "The selected vessel provides very high cargo utilization."
        )
    elif utilization >= 70:
        utilization_message = (
            "The selected vessel provides good cargo utilization."
        )
    else:
        utilization_message = (
            "The selected vessel has relatively lower cargo utilization."
        )

    if distance_nm > 5000:
        distance_message = (
            "The long-distance voyage increases the importance of "
            "large and fuel-efficient vessel selection."
        )
    else:
        distance_message = (
            "The route distance is within a moderate voyage range."
        )

    st.info(
        f"""
        **AI Recommendation:** Charter a **{vessel}**.

        **Why this vessel?**
        - Cargo requirement: **{cargo_quantity:,.0f} MT**
        - Route distance: **{distance_nm:,.0f} nautical miles**
        - Vessel availability: **{vessel_availability}**
        - Vessel utilization: **{utilization:.2f}%**
        - Vessel recommendation score: **{vessel_score}**

        {utilization_message}

        {distance_message}

        Estimated total logistics cost is
        **${cost['total_cost']:,.0f}**.
        """
    )

    st.success(
        f"🚢 AI recommends **{vessel}** for this charter scenario."
    )