def get_smart_action(hour, solar_kw, demand_kw, battery, min_soc_kwh=20.0, reserve_target=80.0):
    reason = ""
    
    # PEAK AWARENESS (Future Planning): 
    # Dopahar 2 baje se 6 baje tak battery bachana hai
    if 14 <= hour < 18:
        if battery.soc_kwh < reserve_target:
            if solar_kw > demand_kw:
                surplus = solar_kw - demand_kw
                charged = battery.charge(surplus, hours=1)
                reason = "PRE-CHARGE: Saving extra solar power for the evening."
                return solar_kw - charged, 0.0, reason
            else:
                reason = "HOLDING BATTERY: Saving battery for later. Using Grid power for now."
                return solar_kw, demand_kw - solar_kw, reason

    # NORMAL RULES (Baaki time ke liye):
    if solar_kw > demand_kw:
        surplus = solar_kw - demand_kw
        charged = battery.charge(surplus, hours=1)
        reason = "EXTRA POWER: Charging the battery with extra solar."
        return solar_kw - charged, 0.0, reason
    else:
        deficit = demand_kw - solar_kw
        available = max(0, battery.soc_kwh - min_soc_kwh)
        taken = min(deficit, available)
        discharged = battery.discharge(taken, hours=1)
        grid_import = deficit - discharged
        
        if discharged > 0:
            reason = f"USING BATTERY: Giving {discharged:.1f} kW from battery to the building."
        else:
            reason = "BATTERY EMPTY: Taking all power from the Government Grid."
            
        return solar_kw + discharged, grid_import, reason