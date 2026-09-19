import streamlit as st

from src.advanced_vessel_recommendation import recommend_vessel
from src.cargo_procurement_recommendation import recommend_procurement
from src.freight_cost_optimizer import calculate_freight_cost
from src.route_risk_analysis import calculate_route_risk


st.set_page_config(
    page_title="AI Explainable Recommendation",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Explainable Recommendation Engine")

st.write(
    "AI-powered freight decision support with transparent explanations "
    "for vessel selection, cargo procurement, logistics cost and route risk."
)

st.divider()


# --------------------------------------------------
# INPUTS
# --------------------------------------------------

st.subheader("📋 Voyage Scenario")

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

    demand_index = st.number_input(
        "📈 Freight Demand Index",
        min_value=0.0,
        max_value=100.0,
        value=85.0,
        step=1.0
    )

    procurement_price = st.number_input(
        "📦 Procurement Price (USD/MT)",
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
        "💰 Freight Rate (USD/MT)",
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
        "🌊 Voyage Duration (Days)",
        min_value=1,
        max_value=100,
        value=12,
        step=1
    )


col1, col2 = st.columns(2)

with col1:

    port_waiting_hours = st.number_input(
        "⚓ Port Waiting Time (Hours)",
        min_value=0,
        max_value=500,
        value=18,
        step=1
    )

with col2:

    port_congestion = st.slider(
        "🚧 Port Congestion",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.05
    )


weather_risk = st.slider(
    "🌦️ Weather Risk",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.05
)


st.divider()


# --------------------------------------------------
# AI ANALYSIS
# --------------------------------------------------

if st.button(
    "🤖 Generate Explainable AI Decision",
    use_container_width=True
):

    # Vessel recommendation
    vessel, vessel_score, utilization = recommend_vessel(
        cargo_quantity,
        distance_nm,
        vessel_availability
    )


    # Procurement recommendation
    (
        procurement_decision,
        procurement_score,
        procurement_percentage,
        recommended_quantity
    ) = recommend_procurement(
        cargo_quantity,
        demand_index,
        procurement_price,
        vessel_availability
    )


    # Freight cost
    cost = calculate_freight_cost(
        cargo_quantity,
        freight_rate,
        bunker_price,
        voyage_days,
        port_waiting_hours,
        procurement_price
    )


    # Route risk
    (
        risk_level,
        risk_score,
        estimated_delay
    ) = calculate_route_risk(
        distance_nm,
        port_congestion,
        weather_risk,
        port_waiting_hours,
        vessel_availability
    )


    # Overall decision score
    overall_score = (
        vessel_score
        + procurement_score
        + (100 - risk_score)
    ) / 3

    overall_score = round(
        overall_score,
        2
    )


    # --------------------------------------------------
    # MAIN RESULTS
    # --------------------------------------------------

    st.success(
        "✅ Explainable AI analysis completed"
    )


    st.subheader("🎯 AI Decision Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🚢 Vessel",
            vessel
        )

    with col2:
        st.metric(
            "📦 Procurement",
            procurement_decision
        )

    with col3:
        st.metric(
            "⚠️ Route Risk",
            risk_level
        )

    with col4:
        st.metric(
            "🧠 AI Score",
            f"{overall_score:.2f}"
        )


    st.divider()


    # --------------------------------------------------
    # VESSEL EXPLANATION
    # --------------------------------------------------

    st.subheader("🚢 Why did AI select this vessel?")

    vessel_reasons = []

    vessel_reasons.append(
        f"Cargo requirement is {cargo_quantity:,.0f} MT."
    )

    vessel_reasons.append(
        f"Recommended vessel is {vessel}."
    )

    vessel_reasons.append(
        f"Expected vessel utilization is {utilization:.2f}%."
    )

    vessel_reasons.append(
        f"Vessel availability in the scenario is {vessel_availability}."
    )

    if distance_nm > 5000:

        vessel_reasons.append(
            "The route is long, so larger and more efficient "
            "bulk vessels receive additional consideration."
        )

    else:

        vessel_reasons.append(
            "The route distance is within a moderate voyage range."
        )


    for reason in vessel_reasons:
        st.write(
            "• " + reason
        )


    st.divider()


    # --------------------------------------------------
    # PROCUREMENT EXPLANATION
    # --------------------------------------------------

    st.subheader(
        "📦 Why did AI recommend this procurement action?"
    )

    procurement_reasons = []

    procurement_reasons.append(
        f"Demand index is {demand_index:.1f}."
    )

    procurement_reasons.append(
        f"Procurement price is ${procurement_price:.2f}/MT."
    )

    procurement_reasons.append(
        f"Vessel availability is {vessel_availability}."
    )

    procurement_reasons.append(
        f"AI procurement score is {procurement_score}."
    )

    procurement_reasons.append(
        f"Recommended procurement quantity is "
        f"{recommended_quantity:,.0f} MT."
    )


    for reason in procurement_reasons:
        st.write(
            "• " + reason
        )


    st.divider()


    # --------------------------------------------------
    # ROUTE RISK EXPLANATION
    # --------------------------------------------------

    st.subheader(
        "⚠️ Why did AI assign this route risk?"
    )

    risk_reasons = []

    risk_reasons.append(
        f"Route distance is {distance_nm:,.0f} nautical miles."
    )

    risk_reasons.append(
        f"Port congestion factor is {port_congestion:.2f}."
    )

    risk_reasons.append(
        f"Weather risk factor is {weather_risk:.2f}."
    )

    risk_reasons.append(
        f"Port waiting time is {port_waiting_hours} hours."
    )

    risk_reasons.append(
        f"Estimated route delay is {estimated_delay:.2f} days."
    )


    for reason in risk_reasons:
        st.write(
            "• " + reason
        )


    st.divider()


    # --------------------------------------------------
    # COST EXPLANATION
    # --------------------------------------------------

    st.subheader(
        "💰 Logistics Cost Explanation"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Freight",
            f"${cost['freight_cost']:,.0f}"
        )

    with col2:
        st.metric(
            "Bunker",
            f"${cost['bunker_cost']:,.0f}"
        )

    with col3:
        st.metric(
            "Port Waiting",
            f"${cost['port_waiting_cost']:,.0f}"
        )

    with col4:
        st.metric(
            "Procurement",
            f"${cost['procurement_cost']:,.0f}"
        )


    st.metric(
        "💵 Total Logistics Cost",
        f"${cost['total_cost']:,.0f}"
    )


    st.divider()


    # --------------------------------------------------
    # FINAL AI EXPLANATION
    # --------------------------------------------------

    st.subheader(
        "🧠 Final Explainable AI Decision"
    )


    st.info(
        f"""
        **Recommended Vessel:** {vessel}

        **Procurement Decision:** {procurement_decision}

        **Route Risk:** {risk_level}

        **Overall AI Score:** {overall_score:.2f}

        **Total Logistics Cost:** ${cost['total_cost']:,.0f}

        The recommendation combines cargo quantity, route distance,
        vessel availability, freight demand, procurement price,
        freight rate, bunker cost, port waiting time, port congestion
        and weather risk.

        Each recommendation is accompanied by the operational factors
        that contributed to the decision, making the AI output easier
        for freight planners and decision-makers to understand.
        """
    )


    st.success(
        "🚢📦🌍 AI recommendation generated with transparent reasoning."
    )
    