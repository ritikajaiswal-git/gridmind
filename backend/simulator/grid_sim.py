import os
import pandas as pd
import matplotlib.pyplot as plt
from solar import get_solar_kw
from demand import get_demand_kw

def run_simulation(days=3):
    data = []
    
    # 3 din matlab 72 ghante (hours) ka loop chalega
    for step in range(days * 24):
        hour_of_day = step % 24  # 24 ke baad wapas 0, 1, 2...
        
        solar = get_solar_kw(hour_of_day)
        demand = get_demand_kw(hour_of_day)
        
        # Ek dictionary mein time, solar aur demand save kar rahe hain
        data.append({
            "hour_index": step,
            "hour_of_day": hour_of_day,
            "solar_kw": solar,
            "demand_kw": demand
        })
        
    df = pd.DataFrame(data)
    
    # Matplotlib ka use karke Graph banate hain
    plt.figure(figsize=(10, 5))
    plt.plot(df["hour_index"], df["solar_kw"], label="Solar Output (kW)", color="green", linewidth=2)
    plt.plot(df["hour_index"], df["demand_kw"], label="Demand (kW)", color="red", linestyle="--")
    plt.title("GridMind: Solar vs Demand (3 Days Simulation)")
    plt.xlabel("Total Hours")
    plt.ylabel("Power (kW)")
    plt.legend()
    plt.grid(True)
    
    # Graph ko save karte hain
    os.makedirs("../data", exist_ok=True)
    save_path = "../data/simulation_graph.png"
    plt.savefig(save_path)
    print(f"Success! Graph saved at: {save_path}")

if __name__ == "__main__":
    run_simulation()