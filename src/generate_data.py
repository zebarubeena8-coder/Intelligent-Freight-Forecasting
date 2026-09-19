import pandas as pd
import numpy as np
import os

# Reproducible results
np.random.seed(42)

# Number of rows
n = 15000

# Date and time
dates = pd.date_range(
    start="2024-01-01",
    periods=n,
    freq="h"
)

# Locations
origins = [
    "Hyderabad", "Mumbai", "Delhi", "Bangalore",
    "Chennai", "Pune", "Kolkata", "Ahmedabad"
]

destinations = [
    "Pune", "Mumbai", "Delhi", "Hyderabad",
    "Bangalore", "Chennai", "Kolkata", "Vijayawada"
]

# Create basic data
data = pd.DataFrame({
    "date": dates,
    "origin": np.random.choice(origins, n),
    "destination": np.random.choice(destinations, n),
    "distance_km": np.random.randint(50, 1800, n),
    "weight_tons": np.round(
        np.random.uniform(1, 40, n), 2
    ),
    "fuel_price": np.round(
        np.random.uniform(85, 115, n), 2
    ),
    "weather_score": np.round(
        np.random.uniform(0, 1, n), 2
    ),
    "traffic_score": np.round(
        np.random.uniform(0, 1, n), 2
    ),
    "holiday": np.random.choice(
        [0, 1],
        n,
        p=[0.9, 0.1]
    )
})

# Extract time-related features
data["month"] = data["date"].dt.month
data["day_of_week"] = data["date"].dt.dayofweek
data["hour"] = data["date"].dt.hour

# Seasonal effect
seasonal_effect = (
    5 * np.sin(2 * np.pi * data["month"] / 12)
)

# Weekend effect
weekend_effect = np.where(
    data["day_of_week"] >= 5,
    -3,
    2
)

# Calculate freight demand
data["freight_demand"] = (
    25
    + (data["weight_tons"] * 2.5)
    + (data["distance_km"] * 0.012)
    - (data["fuel_price"] * 0.08)
    + (data["traffic_score"] * 12)
    + (data["weather_score"] * 6)
    + (data["holiday"] * 10)
    + seasonal_effect
    + weekend_effect
    + np.random.normal(0, 4, n)
)

# Make sure demand is positive
data["freight_demand"] = data["freight_demand"].clip(lower=1)

# Round numerical values
data["freight_demand"] = data["freight_demand"].round(2)

# Create data folder
os.makedirs("data", exist_ok=True)

# Save dataset
file_path = "data/freight_data.csv"
data.to_csv(file_path, index=False)

# Display information
print("========================================")
print(" INTELLIGENT FREIGHT FORECASTING")
print("========================================")
print("Dataset created successfully!")
print("Number of rows:", len(data))
print("Number of columns:", len(data.columns))
print("Dataset shape:", data.shape)
print("Saved to:", file_path)
print("========================================")