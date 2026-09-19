import streamlit as st
from src.cargo_procurement_recommendation import recommend_procurement

st.set_page_config(
    page_title="AI Cargo Procurement",
    page_icon="📦",
    layout="wide"
)

st.title("📦 AI Cargo Procurement Recommendation")
st.write(
    "AI-powered cargo procurement planning based on demand, "
    "price and vessel availability."
)

st.divider()

cargo_quantity = st.number_input(
    "📦 Required Cargo Quantity (MT)",
    min_value=1000,
    max_value=400000,
    value=70000,
    step=1000
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
    min_value=1,
    max_value=1000,
    value=120,
    step=5
)

vessel_availability = st.number_input(
    "🚢 Vessel Availability",
    min_value=1,
    max_value=40,
    value=25,
    step=1
)

if st.button("🤖 Generate Procurement Recommendation", use_container_width=True):

    recommendation, score, percentage, quantity = recommend_procurement(
        cargo_quantity,
        demand_index,
        procurement_price,
        vessel_availability
    )

    st.success(f"Recommendation: {recommendation}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🧠 Procurement Score",
            score
        )

    with col2:
        st.metric(
            "📊 Procurement Percentage",
            f"{percentage}%"
        )

    with col3:
        st.metric(
            "📦 Recommended Quantity",
            f"{quantity:,.0f} MT"
        )

    st.info(
        f"The AI recommends **{recommendation}** for "
        f"**{cargo_quantity:,.0f} MT** of cargo."
    )