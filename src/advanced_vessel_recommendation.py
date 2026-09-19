VESSEL_CAPACITY = {
    "Small Handy": (10000, 30000),
    "Handysize": (20000, 40000),
    "Handymax": (40000, 60000),
    "Supramax": (50000, 65000),
    "Ultramax": (60000, 70000),
    "Panamax": (65000, 85000),
    "Kamsarmax": (75000, 85000),
    "Post-Panamax": (85000, 100000),
    "Capesize": (120000, 180000),
    "Newcastlemax": (180000, 210000),
    "VLOC": (200000, 400000)
}


def recommend_vessel(cargo_quantity, distance_nm, vessel_availability):

    candidates = []

    for vessel, capacity in VESSEL_CAPACITY.items():

        minimum = capacity[0]
        maximum = capacity[1]

        if minimum <= cargo_quantity <= maximum:

            utilization = (cargo_quantity / maximum) * 100

            score = 100

            if utilization >= 80:
                score += 15

            if distance_nm > 5000:
                if vessel in [
                    "Panamax",
                    "Kamsarmax",
                    "Post-Panamax",
                    "Capesize",
                    "Newcastlemax",
                    "VLOC"
                ]:
                    score += 10

            if vessel_availability >= 20:
                score += 10
            elif vessel_availability < 10:
                score -= 15

            candidates.append(
                (vessel, score, utilization)
            )

    if not candidates:
        return "VLOC", 0, 0

    candidates.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return candidates[0]


if __name__ == "__main__":

    cargo = 70000
    distance = 4500
    availability = 25

    vessel, score, utilization = recommend_vessel(
        cargo,
        distance,
        availability
    )

    print("Recommended Vessel:", vessel)
    print("Recommendation Score:", score)
    print("Vessel Utilization:", round(utilization, 2), "%")