# AI Vessel Recommendation Engine
# Recommends a vessel based on cargo quantity and vessel capacity.

VESSEL_CAPACITY = {
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
    "VLOC": (200000, 400000),
}


def recommend_vessel(cargo_quantity):
    """
    Recommend the smallest suitable vessel for the required cargo quantity.
    """

    suitable_vessels = []

    for vessel, (minimum, maximum) in VESSEL_CAPACITY.items():
        if minimum <= cargo_quantity <= maximum:
            suitable_vessels.append((vessel, maximum))

    if suitable_vessels:
        suitable_vessels.sort(key=lambda x: x[1])
        return suitable_vessels[0][0]

    if cargo_quantity < 10000:
        return "Small Handy"

    if cargo_quantity > 400000:
        return "VLOC"

    return "Panamax"


def vessel_utilization(cargo_quantity, vessel):
    """Calculate approximate vessel utilization percentage."""

    if vessel not in VESSEL_CAPACITY:
        return 0

    capacity = VESSEL_CAPACITY[vessel][1]

    utilization = (cargo_quantity / capacity) * 100

    return round(min(utilization, 100), 2)


if __name__ == "__main__":
    quantity = 70000

    recommended = recommend_vessel(quantity)
    utilization = vessel_utilization(quantity, recommended)

    print("Cargo Quantity:", quantity, "MT")
    print("Recommended Vessel:", recommended)
    print("Vessel Utilization:", utilization, "%")