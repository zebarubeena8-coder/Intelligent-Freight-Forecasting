import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Load dataset
data = pd.read_csv("data/freight_data.csv")

# Convert date to datetime
data["date"] = pd.to_datetime(data["date"])

# Sort by date
data = data.sort_values("date")

# Create daily average demand
daily = (
    data.groupby("date")["freight_demand"]
    .mean()
    .reset_index()
)

# Create previous-day demand
daily["lag_1"] = daily["freight_demand"].shift(1)

# Previous 7-day demand
daily["lag_7"] = daily["freight_demand"].shift(7)

# 7-day rolling average
daily["rolling_7"] = (
    daily["freight_demand"]
    .shift(1)
    .rolling(7)
    .mean()
)

# Calendar features
daily["day_of_week"] = daily["date"].dt.dayofweek
daily["month"] = daily["date"].dt.month
daily["day"] = daily["date"].dt.day

# Remove rows with missing values
daily = daily.dropna()

# Features
features = [
    "lag_1",
    "lag_7",
    "rolling_7",
    "day_of_week",
    "month",
    "day"
]

X = daily[features]
y = daily["freight_demand"]

# Chronological train/test split
split = int(len(daily) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

# Create model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

# Train model
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("======================================")
print("TIME SERIES FORECASTING MODEL")
print("======================================")

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R2   : {r2:.2f}")

# Save model
joblib.dump(
    model,
    "models/time_forecasting_model.pkl"
)

print("======================================")
print("Model saved successfully!")
print("Location: models/time_forecasting_model.pkl")
print("======================================")