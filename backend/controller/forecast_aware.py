def get_smart_action(hour, solar_kw, demand_kw, battery, min_soc_kwh=20.0, reserve_target=80.0):
    reason = ""
    
    # PEAK AWARENESS (Future Planning): 
    # Shaam 6 baje (18:00) peak hai. Toh dopahar 14:00 se 17:00 tak battery bachao!
    if 14 <= hour < 18:
        if battery.soc_kwh < reserve_target:
            if solar_kw > demand_kw:
                surplus = solar_kw - demand_kw
                charged = battery.charge(surplus, hours=1)
                reason = "PRE-CHARGE: Shaam ke Peak ke liye solar bachaya jaa raha hai."
                return solar_kw - charged, 0.0, reason
            else:
                # Dhoop kam hai par hum battery nahi denge kyunki shaam aane wali hai!
                reason = "HOLDING RESERVE: Peak aane wala hai, abhi ki demand Grid se le raha hu."
                return solar_kw, demand_kw - solar_kw, reason

    # NORMAL RULES (Baaki time ke liye):
    if solar_kw > demand_kw:
        surplus = solar_kw - demand_kw
        charged = battery.charge(surplus, hours=1)
        reason = "NORMAL SURPLUS: Battery charge ho rahi hai."
        return solar_kw - charged, 0.0, reason
    else:
        deficit = demand_kw - solar_kw
        available = max(0, battery.soc_kwh - min_soc_kwh)
        taken = min(deficit, available)
        discharged = battery.discharge(taken, hours=1)
        grid_import = deficit - discharged
        
        if discharged > 0:
            reason = f"NORMAL DEFICIT: Battery se {discharged:.1f} kW liye."
        else:
            reason = "LOW BATTERY: Poori bijli Grid se le rahe hain."
            
        return solar_kw + discharged, grid_import, reason