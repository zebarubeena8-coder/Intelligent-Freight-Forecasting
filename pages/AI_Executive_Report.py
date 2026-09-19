import streamlit as st
import pandas as pd
from datetime import datetime

from src.advanced_vessel_recommendation import recommend_vessel
from src.cargo_procurement_recommendation import recommend_procurement
from src.freight_cost_optimizer import calculate_freight_cost
from src.route_risk_analysis import calculate_route_risk


st.set_page_config(
    page_title="AI Executive Report",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Freight Executive Report")

st.write(
    "Generate a concise AI-powered decision report for "
    "overseas bulk cargo transportation to East Coast India."
)

st.divider()

st.subheader("📋 Voyage Information")

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
        "🌍 Route Distance (NM)",
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

port_waiting_hours = st.number_input(
    "⚓ Port Waiting Time (hours)",
    min_value=0,
    max_value=500,
    value=18,
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

st.divider()

if st.button(
    "📄 Generate AI Executive Report",
    use_container_width=True
):

    # Vessel
    vessel, vessel_score, utilization = recommend_vessel(
        cargo_quantity,
        distance_nm,
        vessel_availability
    )

    # Procurement
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

    # Cost
    cost = calculate_freight_cost(
        cargo_quantity,
        freight_rate,
        bunker_price,
        voyage_days,
        port_waiting_hours,
        procurement_price
    )

    # Risk
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

    st.success("✅ Executive Report Generated")

    st.subheader("🧠 Executive AI Summary")

    st.info(
        f"""
        The AI analyzed a **{cargo_quantity:,.0f} MT** bulk cargo voyage
        covering **{distance_nm:,.0f} nautical miles**.

        **Vessel:** {vessel}

        **Procurement Action:** {procurement}

        **Recommended Procurement:** {recommended_quantity:,.0f} MT

        **Route Risk:** {risk}

        **Estimated Delay:** {estimated_delay} days

        **Total Logistics Cost:** ${cost['total_cost']:,.0f}

        **Overall AI Decision Score:** {overall_score}
        """
    )

    st.divider()

    st.subheader("📊 Decision Metrics")

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
            "🌍 Route Risk",
            risk
        )

    with col4:
        st.metric(
            "🧠 AI Score",
            overall_score
        )

    st.divider()

    st.subheader("💰 Financial Analysis")

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
            "Procurement Cost",
            f"${cost['procurement_cost']:,.0f}"
        )

    st.metric(
        "Total Logistics Cost",
        f"${cost['total_cost']:,.0f}"
    )

    st.divider()

    st.subheader("⚠️ Operational Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Vessel Utilization",
            f"{utilization:.2f}%"
        )

    with col2:
        st.metric(
            "Route Risk Score",
            f"{risk_score}/100"
        )

    with col3:
        st.metric(
            "Estimated Delay",
            f"{estimated_delay} days"
        )

    # Report data
    report_data = pd.DataFrame([{
        "Generated": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "Cargo Quantity MT": cargo_quantity,
        "Distance NM": distance_nm,
        "Recommended Vessel": vessel,
        "Vessel Utilization %": utilization,
        "Procurement Action": procurement,
        "Recommended Procurement MT": recommended_quantity,
        "Route Risk": risk,
        "Risk Score": risk_score,
        "Estimated Delay Days": estimated_delay,
        "Total Logistics Cost USD": cost["total_cost"],
        "Cost per MT USD": cost["cost_per_mt"],
        "Overall AI Score": overall_score
    }])

    csv_data = report_data.to_csv(index=False)

    st.download_button(
        "⬇️ Download AI Report",
        data=csv_data,
        file_name="AI_Freight_Executive_Report.csv",
        mime="text/csv",
        use_container_width=True
    ) 