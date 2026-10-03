def get_reactive_action(solar_kw, demand_kw, battery, min_soc_kwh=20.0):
    # Rule 1: Dhoop zyada hai (Surplus)
    if solar_kw > demand_kw:
        surplus = solar_kw - demand_kw
        # Bachi hui dhoop se battery charge karo
        charged = battery.charge(surplus, hours=1)
        grid_import = 0.0
        
        # Local system ke paas demand poori karne ke baad kitni energy bachi
        local_supply = solar_kw - charged 
        
    # Rule 2: Dhoop kam hai (Deficit)
    else:
        deficit = demand_kw - solar_kw
        
        # Check karo ki battery mein minimum 20% limit bachi hai ya nahi
        available_to_discharge = max(0, battery.soc_kwh - min_soc_kwh)
        power_to_take = min(deficit, available_to_discharge)
        
        discharged = battery.discharge(power_to_take, hours=1)
        grid_import = deficit - discharged
        
        # Local system kitni energy de paya (Solar + Battery)
        local_supply = solar_kw + discharged 

    return local_supply, grid_import