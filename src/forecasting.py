import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==============================
# 1. Load Dataset
# ==============================

DATA_PATH = "data/freight_data.csv"

data = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Shape:", data.shape)


# ==============================
# 2. Prepare Features
# ==============================

target = "freight_demand"

X = data.drop(columns=[target, "date"])
y = data[target]


# ==============================
# 3. Identify Columns
# ==============================

categorical_features = [
    "origin",
    "destination"
]

numeric_features = [
    "distance_km",
    "weight_tons",
    "fuel_price",
    "weather_score",
    "traffic_score",
    "holiday",
    "month",
    "day_of_week",
    "hour"
]


# ==============================
# 4. Preprocessing
# ==============================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# ==============================
# 5. Machine Learning Model
# ==============================

model = RandomForestRegressor(
    n_estimators=150,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)


# ==============================
# 6. Create Pipeline
# ==============================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==============================
# 7. Split Dataset
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==============================
# 8. Train Model
# ==============================

print("Training Random Forest model...")

pipeline.fit(X_train, y_train)

print("Model training completed!")


# ==============================
# 9. Predictions
# ==============================

predictions = pipeline.predict(X_test)


# ==============================
# 10. Model Evaluation
# ==============================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

r2 = r2_score(
    y_test,
    predictions
)


print("\n========== MODEL RESULTS ==========")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R²  :", round(r2, 4))
print("===================================")


# ==============================
# 11. Save Model
# ==============================

os.makedirs("models", exist_ok=True)

model_path = "models/freight_forecasting_model.pkl"

joblib.dump(
    pipeline,
    model_path
)

print("\nModel saved successfully!")
print("Location:", model_path)