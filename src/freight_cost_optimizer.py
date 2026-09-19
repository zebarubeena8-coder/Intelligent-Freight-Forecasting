def calculate_freight_cost(
    cargo_quantity,
    freight_rate,
    bunker_price,
    voyage_days,
    port_waiting_hours,
    procurement_price
):
    # Ocean freight cost
    freight_cost = cargo_quantity * freight_rate

    # Estimated bunker/fuel consumption
    daily_fuel_consumption = cargo_quantity * 0.00008
    fuel_consumption = daily_fuel_consumption * voyage_days
    bunker_cost = fuel_consumption * bunker_price

    # Port waiting cost
    port_waiting_cost = (
        port_waiting_hours * 5000
    )

    # Cargo procurement cost
    procurement_cost = (
        cargo_quantity * procurement_price
    )

    # Total logistics cost
    total_cost = (
        freight_cost
        + bunker_cost
        + port_waiting_cost
        + procurement_cost
    )

    # Cost per metric ton
    cost_per_mt = total_cost / cargo_quantity

    return {
        "freight_cost": round(freight_cost, 2),
        "bunker_cost": round(bunker_cost, 2),
        "port_waiting_cost": round(port_waiting_cost, 2),
        "procurement_cost": round(procurement_cost, 2),
        "total_cost": round(total_cost, 2),
        "cost_per_mt": round(cost_per_mt, 2)
    }


if __name__ == "__main__":

    result = calculate_freight_cost(
        cargo_quantity=70000,
        freight_rate=35,
        bunker_price=600,
        voyage_days=12,
        port_waiting_hours=18,
        procurement_price=120
    )

    print("===== FREIGHT COST OPTIMIZER =====")
    print("Freight Cost:", result["freight_cost"], "USD")
    print("Bunker Cost:", result["bunker_cost"], "USD")
    print("Port Waiting Cost:", result["port_waiting_cost"], "USD")
    print("Procurement Cost:", result["procurement_cost"], "USD")
    print("Total Logistics Cost:", result["total_cost"], "USD")
    print("Cost per MT:", result["cost_per_mt"], "USD/MT")