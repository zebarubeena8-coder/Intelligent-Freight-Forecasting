import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="AI Freight Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Freight Intelligence Dashboard")

st.write(
    "Interactive analytics dashboard for maritime freight demand, "
    "cargo movement, vessel planning and route intelligence."
)

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/maritime_freight_data.csv")


df = load_data()

st.success("✅ Maritime freight dataset loaded successfully")

# -----------------------------
# KPI SECTION
# -----------------------------

st.subheader("📌 Freight Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📦 Total Cargo",
        f"{df['cargo_quantity_mt'].sum():,.0f} MT"
    )

with col2:
    st.metric(
        "🚢 Average Freight Rate",
        f"${df['freight_rate_usd_mt'].mean():.2f}/MT"
    )

with col3:
    st.metric(
        "🌍 Average Distance",
        f"{df['distance_nm'].mean():,.0f} NM"
    )

with col4:
    st.metric(
        "📈 Average Demand",
        f"{df['freight_demand'].mean():.2f}"
    )

st.divider()

# -----------------------------
# CARGO ANALYSIS
# -----------------------------

st.subheader("📦 Cargo Analysis")

cargo_data = (
    df.groupby("cargo_type")["cargo_quantity_mt"]
    .sum()
    .reset_index()
    .sort_values("cargo_quantity_mt", ascending=False)
)

fig_cargo = px.bar(
    cargo_data.head(10),
    x="cargo_type",
    y="cargo_quantity_mt",
    title="Top Cargo Types by Quantity",
    labels={
        "cargo_type": "Cargo Type",
        "cargo_quantity_mt": "Cargo Quantity (MT)"
    }
)

st.plotly_chart(
    fig_cargo,
    use_container_width=True
)

# -----------------------------
# PORT ANALYSIS
# -----------------------------

st.subheader("⚓ East Coast Port Intelligence")

port_data = (
    df.groupby("destination_port")["cargo_quantity_mt"]
    .sum()
    .reset_index()
    .sort_values("cargo_quantity_mt", ascending=False)
)

fig_port = px.bar(
    port_data,
    x="destination_port",
    y="cargo_quantity_mt",
    title="Cargo Volume by East Coast Indian Port",
    labels={
        "destination_port": "Indian Port",
        "cargo_quantity_mt": "Cargo Quantity (MT)"
    }
)

st.plotly_chart(
    fig_port,
    use_container_width=True
)

# -----------------------------
# COUNTRY ANALYSIS
# -----------------------------

st.subheader("🌍 Overseas Origin Analysis")

country_data = (
    df.groupby("origin_country")["cargo_quantity_mt"]
    .sum()
    .reset_index()
    .sort_values("cargo_quantity_mt", ascending=False)
)

fig_country = px.pie(
    country_data,
    names="origin_country",
    values="cargo_quantity_mt",
    title="Cargo Share by Overseas Origin"
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)

# -----------------------------
# VESSEL ANALYSIS
# -----------------------------

st.subheader("🚢 Vessel Intelligence")

vessel_data = (
    df.groupby("vessel_type")["cargo_quantity_mt"]
    .sum()
    .reset_index()
    .sort_values("cargo_quantity_mt", ascending=False)
)

fig_vessel = px.bar(
    vessel_data,
    x="vessel_type",
    y="cargo_quantity_mt",
    title="Cargo Handled by Vessel Type",
    labels={
        "vessel_type": "Vessel Type",
        "cargo_quantity_mt": "Cargo Quantity (MT)"
    }
)

st.plotly_chart(
    fig_vessel,
    use_container_width=True
)

# -----------------------------
# FREIGHT RATE ANALYSIS
# -----------------------------

st.subheader("💰 Freight Rate Analysis")

fig_rate = px.scatter(
    df.sample(min(1500, len(df))),
    x="distance_nm",
    y="freight_rate_usd_mt",
    color="cargo_type",
    title="Distance vs Freight Rate",
    labels={
        "distance_nm": "Distance (nautical miles)",
        "freight_rate_usd_mt": "Freight Rate (USD/MT)"
    }
)

st.plotly_chart(
    fig_rate,
    use_container_width=True
)

# -----------------------------
# DEMAND ANALYSIS
# -----------------------------

st.subheader("📈 Freight Demand Intelligence")

fig_demand = px.histogram(
    df,
    x="freight_demand",
    nbins=30,
    title="Freight Demand Distribution",
    labels={
        "freight_demand": "Freight Demand"
    }
)

st.plotly_chart(
    fig_demand,
    use_container_width=True
)

# -----------------------------
# RISK INDICATORS
# -----------------------------

st.subheader("⚠️ Maritime Risk Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Port Congestion",
        f"{df['port_congestion'].mean():.2f}"
    )

with col2:
    st.metric(
        "Average Weather Risk",
        f"{df['weather_risk'].mean():.2f}"
    )

with col3:
    st.metric(
        "Average Port Waiting",
        f"{df['port_waiting_hours'].mean():.1f} hrs"
    )

st.divider()

st.success(
    "🧠 Dashboard provides data-driven intelligence for "
    "freight forecasting, vessel chartering and bulk cargo planning."
)