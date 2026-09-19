import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Intelligent Freight Forecasting",
    page_icon="🚚",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA AND MODEL
# --------------------------------------------------

DATA_PATH = "data/freight_data.csv"
MODEL_PATH = "models/freight_forecasting_model.pkl"

data = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)

data["date"] = pd.to_datetime(data["date"])

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🚚 Freight AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🔮 Demand Prediction",
        "📅 7-Day Forecast",
        "📊 Route Analytics",
        "📈 Demand Trends",
        "🤖 Model Information"
    ]
)

# ==================================================
# DASHBOARD
# ==================================================

if page == "🏠 Dashboard":

    st.title("🚚 Intelligent Freight Forecasting")
    st.subheader("AI-Powered Logistics Decision Support System")

    st.write(
        "Analyze freight demand, routes, traffic and weather "
        "using machine learning."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Total Records",
        f"{len(data):,}"
    )

    col2.metric(
        "📊 Average Demand",
        f"{data['freight_demand'].mean():.2f}"
    )

    col3.metric(
        "🚛 Average Weight",
        f"{data['weight_tons'].mean():.2f} tons"
    )

    col4.metric(
        "🛣️ Average Distance",
        f"{data['distance_km'].mean():.0f} km"
    )

    st.divider()

    st.subheader("📈 Freight Demand Trend")

    daily_demand = (
        data.set_index("date")
        .resample("D")["freight_demand"]
        .mean()
    )

    st.line_chart(daily_demand)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏙️ Demand by Origin")

        origin_demand = (
            data.groupby("origin")["freight_demand"]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(origin_demand)

    with col2:

        st.subheader("📍 Demand by Destination")

        destination_demand = (
            data.groupby("destination")["freight_demand"]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(destination_demand)


# ==================================================
# DEMAND PREDICTION
# ==================================================

elif page == "🔮 Demand Prediction":

    st.title("🔮 Freight Demand Prediction")

    st.write(
        "Enter shipment conditions to predict freight demand."
    )

    col1, col2 = st.columns(2)

    with col1:

        origin = st.selectbox(
            "Origin",
            sorted(data["origin"].unique())
        )

        destination = st.selectbox(
            "Destination",
            sorted(data["destination"].unique())
        )

        distance = st.number_input(
            "Distance (km)",
            min_value=10,
            max_value=3000,
            value=500
        )

        weight = st.number_input(
            "Weight (tons)",
            min_value=0.1,
            max_value=50.0,
            value=10.0
        )

        fuel_price = st.number_input(
            "Fuel Price",
            min_value=50.0,
            max_value=200.0,
            value=100.0
        )

    with col2:

        weather_score = st.slider(
            "Weather Score",
            0.0,
            1.0,
            0.5
        )

        traffic_score = st.slider(
            "Traffic Score",
            0.0,
            1.0,
            0.5
        )

        holiday = st.selectbox(
            "Holiday",
            [0, 1]
        )

        month = st.slider(
            "Month",
            1,
            12,
            6
        )

        day_of_week = st.slider(
            "Day of Week",
            0,
            6,
            2
        )

        hour = st.slider(
            "Hour",
            0,
            23,
            12
        )

    if st.button("🚚 Predict Freight Demand"):

        input_data = pd.DataFrame({
            "origin": [origin],
            "destination": [destination],
            "distance_km": [distance],
            "weight_tons": [weight],
            "fuel_price": [fuel_price],
            "weather_score": [weather_score],
            "traffic_score": [traffic_score],
            "holiday": [holiday],
            "month": [month],
            "day_of_week": [day_of_week],
            "hour": [hour]
        })

        prediction = model.predict(input_data)[0]

        st.success(
            f"🚚 Predicted Freight Demand: {prediction:.2f}"
        )

        # AI RECOMMENDATION

        st.subheader("🤖 AI Recommendation")

        if prediction >= 80:

            st.error("🔴 HIGH DEMAND ALERT")

            st.write(
                "Increase vehicle availability, prepare additional "
                "freight capacity and prioritize this route."
            )

        elif prediction >= 50:

            st.warning("🟡 MEDIUM DEMAND ALERT")

            st.write(
                "Maintain sufficient vehicle availability and "
                "monitor demand closely."
            )

        else:

            st.success("🟢 LOW DEMAND")

            st.write(
                "Consider shipment consolidation and optimize "
                "vehicle utilization."
            )


# ==================================================
# 7 DAY FORECAST
# ==================================================

elif page == "📅 7-Day Forecast":

    st.title("📅 7-Day Freight Demand Forecast")

    st.write(
        "AI-based forecasting using previous freight demand "
        "and historical patterns."
    )

    # Load the new forecasting model
    forecast_model = joblib.load(
        "models/time_forecasting_model.pkl"
    )

    # Daily demand
    daily = (
        data.groupby("date")["freight_demand"]
        .mean()
        .sort_index()
    )

    # Last known date
    last_date = daily.index.max()

    # Copy historical demand
    history = daily.copy()

    forecast_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=7,
        freq="D"
    )

    predictions = []

    # Generate 7 future predictions
    for future_date in forecast_dates:

        lag_1 = history.iloc[-1]

        if len(history) >= 7:
            lag_7 = history.iloc[-7]
        else:
            lag_7 = history.mean()

        rolling_7 = history.tail(7).mean()

        input_data = pd.DataFrame({
            "lag_1": [lag_1],
            "lag_7": [lag_7],
            "rolling_7": [rolling_7],
            "day_of_week": [future_date.dayofweek],
            "month": [future_date.month],
            "day": [future_date.day]
        })

        prediction = forecast_model.predict(
            input_data
        )[0]

        predictions.append(prediction)

        # Add prediction to history for next day
        history.loc[future_date] = prediction

    # Create forecast table
    forecast = pd.DataFrame({
        "Date": forecast_dates,
        "Predicted Demand": predictions
    })

    st.subheader("🚚 AI Forecast")

    st.dataframe(
        forecast,
        use_container_width=True
    )

    st.subheader("📈 7-Day Forecast Chart")

    chart_data = forecast.set_index("Date")

    st.line_chart(chart_data)

    st.divider()

    # Average forecast
    average_forecast = forecast[
        "Predicted Demand"
    ].mean()

    st.metric(
        "📊 Average Predicted Demand",
        f"{average_forecast:.2f}"
    )

    # AI recommendation
    st.subheader("🤖 AI Recommendation")

    if average_forecast >= 80:

        st.error(
            "🔴 HIGH DEMAND: Prepare additional "
            "freight capacity and vehicles."
        )

    elif average_forecast >= 50:

        st.warning(
            "🟡 MODERATE DEMAND: Monitor vehicle "
            "availability and route requirements."
        )

    else:

        st.success(
            "🟢 LOWER DEMAND: Consider shipment "
            "consolidation and vehicle optimization."
        )
# ==================================================
# ROUTE ANALYTICS
# ==================================================

elif page == "📊 Route Analytics":

    st.title("📊 Route Analytics")

    data["route"] = (
        data["origin"] + " → " + data["destination"]
    )

    route_data = (
        data.groupby("route")["freight_demand"]
        .mean()
        .sort_values(ascending=False)
    )

    st.subheader("🚛 Average Demand by Route")

    st.bar_chart(
        route_data.head(15)
    )

    st.subheader("📋 Route Data")

    st.dataframe(
        route_data,
        use_container_width=True
    )


# ==================================================
# DEMAND TRENDS
# ==================================================

elif page == "📈 Demand Trends":

    st.title("📈 Demand Trends")

    monthly = (
        data.groupby("month")["freight_demand"]
        .mean()
    )

    st.subheader("📅 Monthly Demand")

    st.line_chart(monthly)

    st.subheader("🚦 Traffic and Demand")

    traffic = (
        data.groupby("traffic_score")["freight_demand"]
        .mean()
    )

    st.line_chart(traffic)


# ==================================================
# MODEL INFORMATION
# ==================================================

elif page == "🤖 Model Information":

    st.title("🤖 Machine Learning Model")

    st.success(
        "Random Forest model loaded successfully."
    )

    st.write(
        "The model predicts freight demand using shipment, "
        "route, traffic, weather and time-related features."
    )

    st.subheader("🧠 Model Inputs")

    st.write(
        "Origin, Destination, Distance, Weight, Fuel Price, "
        "Weather Score, Traffic Score, Holiday, Month, "
        "Day of Week and Hour."
    )

    st.subheader("📊 Dataset")

    st.write(
        f"Total records: {len(data):,}"
    )

    st.write(
        f"Total columns: {len(data.columns)}"
    )

    st.subheader("🚚 Project Purpose")

    st.write(
        "This system helps logistics planners understand "
        "freight demand and make better decisions about "
        "vehicle capacity, routes and shipment planning."
    )

    st.info(
        "Note: The current dataset is synthetic/demo data "
        "created for the project prototype."
    )