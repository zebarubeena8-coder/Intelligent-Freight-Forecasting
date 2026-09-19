def recommend_procurement(
    cargo_quantity,
    demand_index,
    procurement_price,
    vessel_availability
):
    """
    AI-based cargo procurement recommendation.
    """

    score = 0

    # High demand increases procurement priority
    if demand_index >= 80:
        score += 40
    elif demand_index >= 60:
        score += 25
    elif demand_index >= 40:
        score += 10
    else:
        score -= 10

    # Lower procurement price is more attractive
    if procurement_price <= 80:
        score += 30
    elif procurement_price <= 150:
        score += 15
    elif procurement_price <= 250:
        score += 5
    else:
        score -= 15

    # Vessel availability affects logistics readiness
    if vessel_availability >= 20:
        score += 20
    elif vessel_availability >= 10:
        score += 10
    else:
        score -= 10

    # Final recommendation
    if score >= 70:
        recommendation = "Procure Now"
        procurement_percentage = 100
    elif score >= 40:
        recommendation = "Procure Partially"
        procurement_percentage = 60
    else:
        recommendation = "Wait / Monitor Market"
        procurement_percentage = 30

    recommended_quantity = (
        cargo_quantity * procurement_percentage / 100
    )

    return (
        recommendation,
        score,
        procurement_percentage,
        recommended_quantity
    )


if __name__ == "__main__":

    cargo = 70000
    demand = 85
    price = 120
    vessels = 25

    result = recommend_procurement(
        cargo,
        demand,
        price,
        vessels
    )

    recommendation, score, percentage, quantity = result

    print("===== AI CARGO PROCUREMENT =====")
    print("Recommendation:", recommendation)
    print("Procurement Score:", score)
    print("Procurement Percentage:", percentage, "%")
    print("Recommended Quantity:", round(quantity, 2), "MT")