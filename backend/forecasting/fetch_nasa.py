import pandas as pd
import numpy as np
import math
import os

def get_weather_data(days=365):
    data = []
    # 1 saal = 365 din * 24 ghante = 8760 hours ka loop
    for step in range(days * 24):
        hour = step % 24
        day_of_year = (step // 24) % 365
        
        # Sardi (winter) mein dhoop kam aati hai, garmi mein zyada
        season_factor = 1.0 - 0.2 * math.cos(2 * math.pi * day_of_year / 365)
        
        # Din ke waqt bell curve wali dhoop
        if 6 <= hour <= 18:
            fraction = (hour - 6) / 12.0
            irradiance = 1000 * math.sin(fraction * math.pi) * season_factor
        else:
            irradiance = 0
            
        # 20% chance hai ki achanak badal (clouds) aa jayein
        cloud_cover = np.random.uniform(0.2, 0.6) if np.random.random() > 0.8 else 0.0
        
        # Badal ki wajah se dhoop kam ho jayegi
        irradiance = irradiance * (1 - cloud_cover)
        
        # Panel capacity (150kW) aur 85% efficiency ke hisaab se bijli banni
        solar_kw = (irradiance / 1000.0) * 150.0 * 0.85 
        
        data.append({
            "hour_of_day": hour,
            "cloud_cover": cloud_cover,
            "solar_kw": max(0, solar_kw)
        })
        
    df = pd.DataFrame(data)
    
    # Is 1 saal ke data ko CSV mein save kar rahe hain
    os.makedirs(os.path.join(os.path.dirname(__file__), "../data"), exist_ok=True)
    df.to_csv(os.path.join(os.path.dirname(__file__), "../data/historical_weather.csv"), index=False)
    return df