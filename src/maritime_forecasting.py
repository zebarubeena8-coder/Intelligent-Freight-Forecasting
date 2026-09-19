import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# ==========================================
# LOAD MARITIME DATA
# ==========================================

data = pd.read_csv("data/maritime_freight_data.csv")

data["date"] = pd.to_datetime(data["date"])

print("==========================================")
print("MARITIME FREIGHT FORECASTING MODEL")
print("==========================================")

print("Dataset shape:", data.shape)

# ==========================================
# SELECT FEATURES
# ==========================================

features = [
    "cargo_quantity_mt",
    "vessel_capacity_mt",
    "distance_nm",
    "voyage_days",
    "bunker_price_usd_ton",
    "port_congestion",
    "weather_risk",
    "port_waiting_hours",
    "vessel_availability",
    "procurement_price_usd_mt",
    "freight_rate_usd_mt",
    "charter_cost_usd"
]

target = "freight_demand"

X = data[features]
y = data[target]

# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

split = int(len(data) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# ==========================================
# TRAIN RANDOM FOREST MODEL
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ==========================================
# PREDICTION
# ==========================================

predictions = model.predict(X_test)

# ==========================================
# MODEL PERFORMANCE
# ==========================================

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)

print("\n==========================================")
print("MODEL PERFORMANCE")
print("==========================================")

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R2   : {r2:.2f}")

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "models/maritime_forecasting_model.pkl"
)

print("\n==========================================")
print("MODEL SAVED SUCCESSFULLY!")
print("==========================================")

print("Saved to:")
print("models/maritime_forecasting_model.pkl")