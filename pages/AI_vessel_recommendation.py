import streamlit as st
from src.vessel_recommendation import recommend_vessel, vessel_utilization

st.set_page_config(
    page_title="AI Vessel Recommendation",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 AI Vessel Recommendation")
st.write("AI-powered vessel selection based on cargo quantity.")

st.divider()

cargo_quantity = st.number_input(
    "📦 Cargo Quantity (MT)",
    min_value=1000,
    max_value=400000,
    value=70000,
    step=1000
)

if st.button("🤖 Recommend Vessel", use_container_width=True):

    vessel = recommend_vessel(cargo_quantity)
    utilization = vessel_utilization(cargo_quantity, vessel)

    st.success(f"Recommended Vessel: {vessel}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🚢 Recommended Vessel",
            vessel
        )

    with col2:
        st.metric(
            "📊 Vessel Utilization",
            f"{utilization}%"
        )

    st.info(
        f"For a cargo quantity of {cargo_quantity:,.0f} MT, "
        f"the AI recommendation is **{vessel}**."
    )