import random

def get_demand_kw(hour_of_day):
    # 4 Buildings ki demand (Hospital, Apartments, Office, School)
    base_load = 50.0  # Hospital aur fridge wagera hamesha chalte hain
    
    # Shaam ka peak (18:00 - 22:00) jab sab log ghar aate hain
    if 18 <= hour_of_day <= 22:
        peak_load = base_load + 80.0  # Apartments mein AC chalu
        return peak_load * random.uniform(0.95, 1.05)
    
    # Din ka load (9:00 - 17:00) - Office aur School khule hain
    if 9 <= hour_of_day <= 17:
        day_load = base_load + 40.0
        return day_load * random.uniform(0.95, 1.05)
        
    return base_load * random.uniform(0.95, 1.05)