def get_grid_emission_factor():
    # Source: Central Electricity Authority (CEA) India, CO2 Baseline Database (Ver. 19)
    # India ke grid se 1 kWh (unit) lene par ~0.71 kg CO2 nikalta hai.
    return 0.71

def get_solar_emission_factor():
    # Solar energy green hoti hai, toh direct pollution 0.0 hai
    return 0.0