import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="AI Freight Demand Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Freight Demand Analytics")

st.write(
    "Analyze freight demand patterns across cargo types, "
    "overseas origins, East Coast Indian ports and freight rates."
)

st.divider()


# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/maritime_freight_data.csv")


df = load_data()


# -----------------------------
# FILTERS
# -----------------------------

st.subheader("🔎 Demand Filters")

col1, col2 = st.columns(2)

with col1:
    cargo_type = st.selectbox(
        "📦 Cargo Type",
        ["All"] + sorted(df["cargo_type"].unique().tolist())
    )

with col2:
    country = st.selectbox(
        "🌎 Origin Country",
        ["All"] + sorted(df["origin_country"].unique().tolist())
    )


filtered_df = df.copy()

if cargo_type != "All":
    filtered_df = filtered_df[
        filtered_df["cargo_type"] == cargo_type
    ]

if country != "All":
    filtered_df = filtered_df[
        filtered_df["origin_country"] == country
    ]


st.divider()


# -----------------------------
# KPI CARDS
# -----------------------------

st.subheader("📊 Demand Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📈 Average Demand",
        f"{filtered_df['freight_demand'].mean():.2f}"
    )

with col2:
    st.metric(
        "📦 Total Cargo",
        f"{filtered_df['cargo_quantity_mt'].sum():,.0f} MT"
    )

with col3:
    st.metric(
        "💰 Avg Freight Rate",
        f"${filtered_df['freight_rate_usd_mt'].mean():.2f}/MT"
    )

with col4:
    st.metric(
        "🚢 Avg Vessel Availability",
        f"{filtered_df['vessel_availability'].mean():.1f}"
    )


st.divider()


# -----------------------------
# DEMAND CLASSIFICATION
# -----------------------------

average_demand = filtered_df["freight_demand"].mean()

if average_demand >= 80:
    demand_status = "High Demand"
elif average_demand >= 50:
    demand_status = "Moderate Demand"
else:
    demand_status = "Low Demand"


st.subheader("🤖 AI Demand Assessment")

if demand_status == "High Demand":
    st.success(
        f"🔥 {demand_status}: Current data indicates strong freight demand."
    )

elif demand_status == "Moderate Demand":
    st.warning(
        f"⚠️ {demand_status}: Freight demand is at a moderate level."
    )

else:
    st.info(
        f"📉 {demand_status}: Freight demand is relatively low."
    )


# -----------------------------
# DEMAND DISTRIBUTION
# -----------------------------

st.subheader("📈 Freight Demand Distribution")

fig_demand = px.histogram(
    filtered_df,
    x="freight_demand",
    nbins=30,
    title="Distribution of Freight Demand",
    labels={
        "freight_demand": "Freight Demand"
    }
)

st.plotly_chart(
    fig_demand,
    use_container_width=True
)


# -----------------------------
# CARGO DEMAND
# -----------------------------

st.subheader("📦 Demand by Cargo Type")

cargo_demand = (
    filtered_df
    .groupby("cargo_type")["freight_demand"]
    .mean()
    .reset_index()
    .sort_values(
        "freight_demand",
        ascending=False
    )
)

fig_cargo = px.bar(
    cargo_demand,
    x="cargo_type",
    y="freight_demand",
    title="Average Freight Demand by Cargo",
    labels={
        "cargo_type": "Cargo Type",
        "freight_demand": "Average Demand"
    }
)

st.plotly_chart(
    fig_cargo,
    use_container_width=True
)


# -----------------------------
# COUNTRY DEMAND
# -----------------------------

st.subheader("🌎 Demand by Overseas Country")

country_demand = (
    filtered_df
    .groupby("origin_country")["freight_demand"]
    .mean()
    .reset_index()
    .sort_values(
        "freight_demand",
        ascending=False
    )
)

fig_country = px.bar(
    country_demand,
    x="origin_country",
    y="freight_demand",
    title="Average Freight Demand by Origin Country",
    labels={
        "origin_country": "Origin Country",
        "freight_demand": "Average Demand"
    }
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)


# -----------------------------
# PORT DEMAND
# -----------------------------

st.subheader("⚓ Demand by Indian Port")

port_demand = (
    filtered_df
    .groupby("destination_port")["freight_demand"]
    .mean()
    .reset_index()
    .sort_values(
        "freight_demand",
        ascending=False
    )
)

fig_port = px.bar(
    port_demand,
    x="destination_port",
    y="freight_demand",
    title="Average Freight Demand by East Coast Port",
    labels={
        "destination_port": "Indian Port",
        "freight_demand": "Average Demand"
    }
)

st.plotly_chart(
    fig_port,
    use_container_width=True
)


# -----------------------------
# DEMAND VS FREIGHT RATE
# -----------------------------

st.subheader("💰 Demand vs Freight Rate")

sample_df = filtered_df.sample(
    min(1500, len(filtered_df)),
    random_state=42
)

fig_rate = px.scatter(
    sample_df,
    x="freight_rate_usd_mt",
    y="freight_demand",
    color="cargo_type",
    title="Freight Rate vs Demand",
    labels={
        "freight_rate_usd_mt": "Freight Rate (USD/MT)",
        "freight_demand": "Freight Demand"
    }
)

st.plotly_chart(
    fig_rate,
    use_container_width=True
)


# -----------------------------
# TOP DEMAND CARGO
# -----------------------------

st.divider()

st.subheader("🏆 Highest-Demand Cargo Types")

top_cargo = cargo_demand.head(5).copy()

top_cargo["freight_demand"] = (
    top_cargo["freight_demand"].round(2)
)

st.dataframe(
    top_cargo,
    use_container_width=True,
    hide_index=True
)


# -----------------------------
# AI INSIGHT
# -----------------------------

st.subheader("🧠 AI Market Insight")

if len(cargo_demand) > 0:

    highest_demand_cargo = cargo_demand.iloc[0]["cargo_type"]
    highest_demand_value = cargo_demand.iloc[0]["freight_demand"]

    st.info(
        f"""
        Based on the selected filters, the average freight demand is
        **{average_demand:.2f}**.

        The highest average demand in the filtered dataset is for
        **{highest_demand_cargo}**, with a demand value of
        **{highest_demand_value:.2f}**.

        Current demand classification:
        **{demand_status}**.
        """
    )
else:

    st.warning(
        "No data is available for the selected filters."
    )