import streamlit as st
from src.freight_cost_optimizer import calculate_freight_cost

st.set_page_config(
    page_title="AI Freight Cost Optimizer",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Freight Cost Optimizer")
st.write(
    "Estimate total logistics cost for overseas bulk cargo transportation."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    cargo_quantity = st.number_input(
        "📦 Cargo Quantity (MT)",
        min_value=1000,
        max_value=400000,
        value=70000,
        step=1000
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

with col2:
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

if st.button(
    "💰 Calculate Total Logistics Cost",
    use_container_width=True
):

    result = calculate_freight_cost(
        cargo_quantity,
        freight_rate,
        bunker_price,
        voyage_days,
        port_waiting_hours,
        procurement_price
    )

    st.success("✅ Cost Analysis Completed")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚢 Freight Cost",
            f"${result['freight_cost']:,.0f}"
        )

    with col2:
        st.metric(
            "⛽ Bunker Cost",
            f"${result['bunker_cost']:,.0f}"
        )

    with col3:
        st.metric(
            "⚓ Port Waiting Cost",
            f"${result['port_waiting_cost']:,.0f}"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📦 Procurement Cost",
            f"${result['procurement_cost']:,.0f}"
        )

    with col2:
        st.metric(
            "💰 Total Logistics Cost",
            f"${result['total_cost']:,.0f}"
        )

    with col3:
        st.metric(
            "📊 Cost per MT",
            f"${result['cost_per_mt']:.2f}"
        )

    st.info(
        f"Estimated total logistics cost for "
        f"**{cargo_quantity:,.0f} MT** is "
        f"**${result['total_cost']:,.0f}**."
    )
    