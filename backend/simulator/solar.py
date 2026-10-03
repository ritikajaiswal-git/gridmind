import math
import random

def get_solar_kw(hour_of_day, capacity_kw=150.0):
    # Dhoop subah 6 baje aati hai aur shaam 18:00 (6 PM) chali jati hai
    if 6 <= hour_of_day <= 18:
        # Pahaad (bell curve) jaisi shape banane ke liye hum Sine wave use kar rahe hain
        fraction = (hour_of_day - 6) / 12.0
        ideal_power = capacity_kw * math.sin(fraction * math.pi)
        
        # Thoda badal (clouds) ka effect daalne ke liye 90% se 100% ke beech random power
        cloud_factor = random.uniform(0.9, 1.0)
        return ideal_power * cloud_factor
    
    return 0.0