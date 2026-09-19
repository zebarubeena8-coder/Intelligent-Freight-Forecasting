import streamlit as st
from src.advanced_vessel_recommendation import recommend_vessel

st.set_page_config(
    page_title="Advanced AI Vessel Recommendation",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 Advanced AI Vessel Recommendation")
st.write(
    "AI-powered vessel selection using cargo quantity, "
    "route distance, and vessel availability."
)

st.divider()

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

vessel_availability = st.number_input(
    "🚢 Vessel Availability",
    min_value=1,
    max_value=40,
    value=25,
    step=1
)

if st.button("🤖 Generate AI Recommendation", use_container_width=True):

    vessel, score, utilization = recommend_vessel(
        cargo_quantity,
        distance_nm,
        vessel_availability
    )

    st.success(f"Recommended Vessel: {vessel}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚢 Recommended Vessel",
            vessel
        )

    with col2:
        st.metric(
            "🧠 Recommendation Score",
            score
        )

    with col3:
        st.metric(
            "📊 Vessel Utilization",
            f"{utilization:.2f}%"
        )

    st.info(
        f"For **{cargo_quantity:,.0f} MT** cargo over a route of "
        f"**{distance_nm:,.0f} nautical miles**, with **{vessel_availability}** "
        f"vessels available, the AI recommends **{vessel}**."
    )