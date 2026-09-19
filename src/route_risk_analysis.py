def calculate_route_risk(
    distance_nm,
    port_congestion,
    weather_risk,
    port_waiting_hours,
    vessel_availability
):
    score = 0

    # Distance risk
    if distance_nm >= 8000:
        score += 25
    elif distance_nm >= 5000:
        score += 15
    else:
        score += 5

    # Port congestion risk
    score += port_congestion * 25

    # Weather risk
    score += weather_risk * 25

    # Port waiting risk
    if port_waiting_hours >= 48:
        score += 20
    elif port_waiting_hours >= 24:
        score += 10
    else:
        score += 5

    # Vessel availability
    if vessel_availability < 10:
        score += 15
    elif vessel_availability < 20:
        score += 8

    score = round(min(score, 100), 2)

    if score >= 70:
        risk_level = "High Risk"
    elif score >= 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    estimated_delay = round(
        (score / 100) * 5,
        2
    )

    return risk_level, score, estimated_delay


if __name__ == "__main__":

    risk, score, delay = calculate_route_risk(
        distance_nm=4500,
        port_congestion=0.4,
        weather_risk=0.3,
        port_waiting_hours=18,
        vessel_availability=25
    )

    print("===== ROUTE RISK ANALYSIS =====")
    print("Risk Level:", risk)
    print("Risk Score:", score)
    print("Estimated Delay:", delay, "days")