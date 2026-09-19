from vessel_recommendation import recommend_vessel, vessel_utilization

cargo_quantity = 70000

vessel = recommend_vessel(cargo_quantity)
utilization = vessel_utilization(cargo_quantity, vessel)

print("===== AI VESSEL RECOMMENDATION =====")
print("Cargo Quantity:", cargo_quantity, "MT")
print("Recommended Vessel:", vessel)
print("Vessel Utilization:", utilization, "%")