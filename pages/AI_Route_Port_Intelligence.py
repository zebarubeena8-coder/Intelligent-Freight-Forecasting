import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="AI Route Port Intelligence",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 AI Route & Port Intelligence")

st.write(
    "Analyze overseas-to-East-Coast maritime routes, "
    "cargo flows, port congestion and operational conditions."
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

st.subheader("🔎 Route Filters")

col1, col2, col3 = st.columns(3)

with col1:
    country = st.selectbox(
        "🌎 Overseas Country",
        ["All"] + sorted(df["origin_country"].unique().tolist())
    )

with col2:
    destination = st.selectbox(
        "⚓ East Coast Indian Port",
        ["All"] + sorted(df["destination_port"].unique().tolist())
    )

with col3:
    cargo = st.selectbox(
        "📦 Cargo Type",
        ["All"] + sorted(df["cargo_type"].unique().tolist())
    )


filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[
        filtered_df["origin_country"] == country
    ]

if destination != "All":
    filtered_df = filtered_df[
        filtered_df["destination_port"] == destination
    ]

if cargo != "All":
    filtered_df = filtered_df[
        filtered_df["cargo_type"] == cargo
    ]


st.divider()


# -----------------------------
# ROUTE KPIs
# -----------------------------

st.subheader("📊 Route Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📦 Cargo Volume",
        f"{filtered_df['cargo_quantity_mt'].sum():,.0f} MT"
    )

with col2:
    st.metric(
        "🌍 Avg Distance",
        f"{filtered_df['distance_nm'].mean():,.0f} NM"
    )

with col3:
    st.metric(
        "⚓ Avg Congestion",
        f"{filtered_df['port_congestion'].mean():.2f}"
    )

with col4:
    st.metric(
        "⏱️ Avg Waiting",
        f"{filtered_df['port_waiting_hours'].mean():.1f} hrs"
    )


st.divider()


# -----------------------------
# ROUTE TABLE
# -----------------------------

st.subheader("🛳️ Route Details")

route_columns = [
    "origin_country",
    "origin_port",
    "destination_port",
    "cargo_type",
    "distance_nm",
    "voyage_days",
    "port_congestion",
    "weather_risk",
    "port_waiting_hours"
]

available_columns = [
    col for col in route_columns
    if col in filtered_df.columns
]

st.dataframe(
    filtered_df[available_columns].head(100),
    use_container_width=True
)


# -----------------------------
# PORT CONGESTION
# -----------------------------

st.subheader("⚓ Port Congestion Analysis")

port_congestion = (
    filtered_df
    .groupby("destination_port")["port_congestion"]
    .mean()
    .reset_index()
    .sort_values("port_congestion", ascending=False)
)

fig_congestion = px.bar(
    port_congestion,
    x="destination_port",
    y="port_congestion",
    title="Average Port Congestion",
    labels={
        "destination_port": "Indian Port",
        "port_congestion": "Average Congestion"
    }
)

st.plotly_chart(
    fig_congestion,
    use_container_width=True
)


# -----------------------------
# DISTANCE VS VOYAGE
# -----------------------------

st.subheader("🌊 Distance vs Voyage Duration")

fig_voyage = px.scatter(
    filtered_df.sample(
        min(1500, len(filtered_df))
    ),
    x="distance_nm",
    y="voyage_days",
    color="destination_port",
    title="Route Distance vs Voyage Duration",
    labels={
        "distance_nm": "Distance (nautical miles)",
        "voyage_days": "Voyage Duration (days)"
    }
)

st.plotly_chart(
    fig_voyage,
    use_container_width=True
)


# -----------------------------
# WEATHER RISK
# -----------------------------

st.subheader("🌦️ Weather Risk by Port")

weather_data = (
    filtered_df
    .groupby("destination_port")["weather_risk"]
    .mean()
    .reset_index()
)

fig_weather = px.bar(
    weather_data,
    x="destination_port",
    y="weather_risk",
    title="Average Weather Risk by Port",
    labels={
        "destination_port": "Indian Port",
        "weather_risk": "Weather Risk"
    }
)

st.plotly_chart(
    fig_weather,
    use_container_width=True
)


# -----------------------------
# AI INSIGHT
# -----------------------------

st.divider()

st.subheader("🤖 AI Route Insight")

if len(filtered_df) == 0:

    st.error(
        "No routes found for the selected filters."
    )

else:

    highest_congestion_port = (
        port_congestion.iloc[0]["destination_port"]
    )

    average_distance = filtered_df["distance_nm"].mean()
    average_waiting = filtered_df["port_waiting_hours"].mean()

    st.info(
        f"Based on the selected route filters, the average voyage "
        f"distance is **{average_distance:,.0f} nautical miles** "
        f"and average port waiting time is **{average_waiting:.1f} hours**. "
        f"The highest average congestion in the filtered data is at "
        f"**{highest_congestion_port}**."
    )