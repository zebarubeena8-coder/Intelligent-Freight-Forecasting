import pandas as pd
import numpy as np

np.random.seed(42)

# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

N = 15000

# ---------------------------------------------------------
# OVERSEAS PORTS AND COUNTRIES
# ---------------------------------------------------------

port_country = {
    # Australia
    "Newcastle": "Australia",
    "Port Kembla": "Australia",
    "Gladstone": "Australia",
    "Hay Point": "Australia",
    "Dalrymple Bay": "Australia",
    "Port Hedland": "Australia",

    # Indonesia
    "Tanjung Bara": "Indonesia",
    "Taboneo": "Indonesia",
    "Balikpapan": "Indonesia",

    # South Africa
    "Richards Bay": "South Africa",
    "Durban": "South Africa",
    "Saldanha Bay": "South Africa",

    # Brazil
    "Tubarão": "Brazil",
    "Itaguai": "Brazil",
    "Santos": "Brazil",

    # USA
    "Hampton Roads": "USA",
    "New Orleans": "USA",
    "Houston": "USA",

    # Canada
    "Vancouver": "Canada",
    "Prince Rupert": "Canada",
    "Quebec": "Canada",

    # Russia
    "Vostochny": "Russia",
    "Nakhodka": "Russia",

    # Mozambique
    "Maputo": "Mozambique",
    "Beira": "Mozambique",

    # Colombia
    "Puerto Bolivar": "Colombia",
    "Cartagena": "Colombia",

    # Vietnam
    "Vung Tau": "Vietnam",
    "Cam Pha": "Vietnam"
}

origin_ports = list(port_country.keys())

# ---------------------------------------------------------
# EAST COAST INDIA DESTINATION PORTS
# ---------------------------------------------------------

destination_ports = [
    "Paradip",
    "Dhamra",
    "Visakhapatnam",
    "Gangavaram",
    "Kakinada",
    "Krishnapatnam",
    "Chennai",
    "Kamarajar"
]

# ---------------------------------------------------------
# BULK CARGO TYPES
# ---------------------------------------------------------

cargo_types = [
    "Thermal Coal",
    "Coking Coal",
    "Iron Ore",
    "Iron Ore Pellets",
    "Limestone",
    "Bauxite",
    "Alumina",
    "Fertilizer",
    "Rock Phosphate",
    "Petcoke",
    "Gypsum",
    "Manganese Ore",
    "Nickel Ore",
    "Wheat",
    "Corn",
    "Soybean",
    "Sugar"
]

# ---------------------------------------------------------
# VESSEL TYPES + APPROXIMATE CAPACITY RANGES
# Synthetic prototype ranges
# ---------------------------------------------------------

vessel_capacity_ranges = {
    "Small Handy": (10000, 30000),
    "Handysize": (20000, 40000),
    "Handymax": (40000, 60000),
    "Supramax": (50000, 65000),
    "Ultramax": (60000, 70000),
    "Panamax": (65000, 85000),
    "Kamsarmax": (75000, 85000),
    "Post-Panamax": (85000, 100000),
    "Newcastlemax": (180000, 210000),
    "Capesize": (120000, 180000),
    "VLOC": (200000, 400000)
}

vessel_types = list(vessel_capacity_ranges.keys())

# ---------------------------------------------------------
# CARGO PROCUREMENT PRICE RANGES
# Synthetic prototype values in USD/MT
# ---------------------------------------------------------

cargo_price_ranges = {
    "Thermal Coal": (65, 110),
    "Coking Coal": (120, 190),
    "Iron Ore": (80, 140),
    "Iron Ore Pellets": (100, 160),
    "Limestone": (25, 50),
    "Bauxite": (40, 75),
    "Alumina": (200, 350),
    "Fertilizer": (180, 350),
    "Rock Phosphate": (100, 180),
    "Petcoke": (80, 140),
    "Gypsum": (20, 45),
    "Manganese Ore": (120, 220),
    "Nickel Ore": (45, 90),
    "Wheat": (180, 300),
    "Corn": (160, 280),
    "Soybean": (350, 500),
    "Sugar": (350, 600)
}

# ---------------------------------------------------------
# APPROXIMATE DISTANCE BASES
# Synthetic route-distance model in nautical miles
# ---------------------------------------------------------

origin_distance = {
    "Newcastle": 4000,
    "Port Kembla": 4050,
    "Gladstone": 3900,
    "Hay Point": 4000,
    "Dalrymple Bay": 4000,
    "Port Hedland": 4300,

    "Tanjung Bara": 2700,
    "Taboneo": 2800,
    "Balikpapan": 2850,

    "Richards Bay": 5000,
    "Durban": 5100,
    "Saldanha Bay": 5300,

    "Tubarão": 8500,
    "Itaguai": 8400,
    "Santos": 8300,

    "Hampton Roads": 9500,
    "New Orleans": 9000,
    "Houston": 9100,

    "Vancouver": 9800,
    "Prince Rupert": 9600,
    "Quebec": 10500,

    "Vostochny": 3500,
    "Nakhodka": 3450,

    "Maputo": 4800,
    "Beira": 4600,

    "Puerto Bolivar": 9000,
    "Cartagena": 9100,

    "Vung Tau": 2300,
    "Cam Pha": 2200
}

destination_distance_adjustment = {
    "Paradip": 0,
    "Dhamra": 50,
    "Visakhapatnam": 200,
    "Gangavaram": 220,
    "Kakinada": 300,
    "Krishnapatnam": 450,
    "Chennai": 500,
    "Kamarajar": 520
}

# ---------------------------------------------------------
# PORT CONGESTION BASELINES
# Synthetic values between 0 and 1
# ---------------------------------------------------------

port_congestion_base = {
    "Paradip": 0.45,
    "Dhamra": 0.35,
    "Visakhapatnam": 0.50,
    "Gangavaram": 0.40,
    "Kakinada": 0.38,
    "Krishnapatnam": 0.42,
    "Chennai": 0.65,
    "Kamarajar": 0.55
}

# ---------------------------------------------------------
# VESSEL SPEED RANGES
# Knots
# ---------------------------------------------------------

vessel_speed_ranges = {
    "Small Handy": (10.5, 12.5),
    "Handysize": (11, 13),
    "Handymax": (11, 13),
    "Supramax": (11, 14),
    "Ultramax": (11, 14),
    "Panamax": (11, 14),
    "Kamsarmax": (11, 14),
    "Post-Panamax": (11, 14),
    "Newcastlemax": (12, 15),
    "Capesize": (12, 15),
    "VLOC": (11, 14)
}

# ---------------------------------------------------------
# RANDOM BASIC VARIABLES
# ---------------------------------------------------------

dates = np.random.choice(
    pd.date_range("2023-01-01", "2026-08-31", freq="D"),
    size=N
)

origin_port = np.random.choice(origin_ports, size=N)
destination_port = np.random.choice(destination_ports, size=N)
cargo_type = np.random.choice(cargo_types, size=N)
vessel_type = np.random.choice(vessel_types, size=N)

origin_country = [
    port_country[p]
    for p in origin_port
]

# ---------------------------------------------------------
# CARGO QUANTITY
# ---------------------------------------------------------

cargo_quantity_mt = np.random.randint(
    10000,
    300001,
    size=N
)

# ---------------------------------------------------------
# VESSEL CAPACITY BASED ON VESSEL TYPE
# ---------------------------------------------------------

vessel_capacity_mt = np.array([
    np.random.uniform(
        vessel_capacity_ranges[v][0],
        vessel_capacity_ranges[v][1]
    )
    for v in vessel_type
])

vessel_capacity_mt = np.round(
    vessel_capacity_mt
).astype(int)

# ---------------------------------------------------------
# DISTANCE
# ---------------------------------------------------------

distance_nm = np.array([
    origin_distance[o]
    + destination_distance_adjustment[d]
    + np.random.normal(0, 120)
    for o, d in zip(origin_port, destination_port)
])

distance_nm = np.clip(
    distance_nm,
    1500,
    11000
)

distance_nm = np.round(distance_nm).astype(int)

# ---------------------------------------------------------
# VOYAGE SPEED + VOYAGE DAYS
# ---------------------------------------------------------

speed_knots = np.array([
    np.random.uniform(
        vessel_speed_ranges[v][0],
        vessel_speed_ranges[v][1]
    )
    for v in vessel_type
])

# 24 nautical miles per day per knot
voyage_days = (
    distance_nm / (speed_knots * 24)
) * 1.12

voyage_days = np.round(
    voyage_days,
    1
)

# ---------------------------------------------------------
# BUNKER PRICE
# ---------------------------------------------------------

bunker_price_usd_ton = np.random.uniform(
    450,
    800,
    N
)

bunker_price_usd_ton = np.round(
    bunker_price_usd_ton,
    2
)

# ---------------------------------------------------------
# PORT CONGESTION
# ---------------------------------------------------------

port_congestion = np.array([
    port_congestion_base[p]
    + np.random.normal(0, 0.12)
    for p in destination_port
])

port_congestion = np.clip(
    port_congestion,
    0,
    1
)

port_congestion = np.round(
    port_congestion,
    3
)

# ---------------------------------------------------------
# WEATHER RISK
# ---------------------------------------------------------

months = pd.to_datetime(dates).month

weather_risk = np.random.uniform(
    0.05,
    0.75,
    N
)

# Add seasonal risk variation
monsoon = np.isin(
    months,
    [6, 7, 8, 9]
)

weather_risk[monsoon] += 0.12

weather_risk = np.clip(
    weather_risk,
    0,
    1
)

weather_risk = np.round(
    weather_risk,
    3
)

# ---------------------------------------------------------
# PORT WAITING HOURS
# ---------------------------------------------------------

port_waiting_hours = (
    8
    + port_congestion * 80
    + np.random.normal(0, 12, N)
)

port_waiting_hours = np.clip(
    port_waiting_hours,
    4,
    140
)

port_waiting_hours = np.round(
    port_waiting_hours,
    1
)

# ---------------------------------------------------------
# VESSEL AVAILABILITY
# Number of suitable vessels available
# ---------------------------------------------------------

vessel_availability = np.random.randint(
    1,
    41,
    N
)

# ---------------------------------------------------------
# PROCUREMENT PRICE
# ---------------------------------------------------------

procurement_price_usd_mt = np.array([
    np.random.uniform(
        cargo_price_ranges[c][0],
        cargo_price_ranges[c][1]
    )
    for c in cargo_type
])

procurement_price_usd_mt = np.round(
    procurement_price_usd_mt,
    2
)

# ---------------------------------------------------------
# FREIGHT RATE
# Synthetic prototype formula
# ---------------------------------------------------------

size_factor = np.array([
    {
        "Small Handy": 1.20,
        "Handysize": 1.15,
        "Handymax": 1.10,
        "Supramax": 1.05,
        "Ultramax": 1.00,
        "Panamax": 0.95,
        "Kamsarmax": 0.92,
        "Post-Panamax": 0.90,
        "Newcastlemax": 0.82,
        "Capesize": 0.78,
        "VLOC": 0.72
    }[v]
    for v in vessel_type
])

freight_rate_usd_mt = (
    8
    + distance_nm * 0.0018
    + bunker_price_usd_ton * 0.012
    + port_congestion * 8
    + weather_risk * 3
    + size_factor * 4
    + np.random.normal(0, 1.5, N)
)

freight_rate_usd_mt = np.clip(
    freight_rate_usd_mt,
    10,
    60
)

freight_rate_usd_mt = np.round(
    freight_rate_usd_mt,
    2
)

# ---------------------------------------------------------
# CHARTER COST
# ---------------------------------------------------------

charter_cost_usd = (
    freight_rate_usd_mt
    * cargo_quantity_mt
)

charter_cost_usd = np.round(
    charter_cost_usd,
    2
)

# ---------------------------------------------------------
# FREIGHT DEMAND INDEX
# Synthetic target for ML model
# ---------------------------------------------------------

freight_demand = (
    25
    + cargo_quantity_mt * 0.00025
    + vessel_availability * 0.8
    + (1 - port_congestion) * 10
    + (1 - weather_risk) * 6
    - freight_rate_usd_mt * 0.35
    + np.random.normal(0, 5, N)
)

freight_demand = np.clip(
    freight_demand,
    0,
    None
)

freight_demand = np.round(
    freight_demand,
    2
)

# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------

data = pd.DataFrame({
    "date": pd.to_datetime(dates),

    "origin_country": origin_country,
    "origin_port": origin_port,
    "destination_port": destination_port,

    "cargo_type": cargo_type,
    "cargo_quantity_mt": cargo_quantity_mt,

    "vessel_type": vessel_type,
    "vessel_capacity_mt": vessel_capacity_mt,

    "distance_nm": distance_nm,
    "voyage_days": voyage_days,

    "bunker_price_usd_ton": bunker_price_usd_ton,

    "port_congestion": port_congestion,
    "weather_risk": weather_risk,
    "port_waiting_hours": port_waiting_hours,

    "vessel_availability": vessel_availability,

    "procurement_price_usd_mt": procurement_price_usd_mt,

    "freight_rate_usd_mt": freight_rate_usd_mt,

    "charter_cost_usd": charter_cost_usd,

    "freight_demand": freight_demand
})

# ---------------------------------------------------------
# SORT DATA
# ---------------------------------------------------------

data = data.sort_values(
    "date"
).reset_index(drop=True)

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

output_path = "data/maritime_freight_data.csv"

data.to_csv(
    output_path,
    index=False
)

# ---------------------------------------------------------
# INFORMATION
# ---------------------------------------------------------

print("\n==============================================")
print("MARITIME DATASET CREATED SUCCESSFULLY")
print("==============================================")

print("Rows:", len(data))
print("Columns:", len(data.columns))

print("\nCountries:")
print(data["origin_country"].nunique())

print("\nOverseas Ports:")
print(data["origin_port"].nunique())

print("\nIndian East Coast Ports:")
print(data["destination_port"].nunique())

print("\nCargo Types:")
print(data["cargo_type"].nunique())

print("\nVessel Types:")
print(data["vessel_type"].nunique())

print("\nDataset shape:")
print(data.shape)

print("\nSaved to:")
print(output_path)

print("==============================================")