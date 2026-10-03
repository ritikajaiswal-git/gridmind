import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# Dusre folders ka code use karne ke liye path set kar rahe hain
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.solar import get_solar_kw
from simulator.demand import get_demand_kw
from simulator.battery import Battery
from simulator.frequency import GridFrequency
from reactive import get_reactive_action

def run_comparison(days=3):
    data = []
    battery = Battery(capacity=100.0, max_power=50.0)
    freq_no_battery = GridFrequency()
    freq_with_battery = GridFrequency()
    
    for step in range(days * 24):
        hour = step % 24
        solar = get_solar_kw(hour)
        demand = get_demand_kw(hour)
        
        # SCENARIO 1: Bina Battery (Pura load grid par)
        local_supply_no_bat = solar
        f_no = freq_no_battery.update(local_supply_no_bat, demand)
        
        # SCENARIO 2: Reactive Controller aur Battery ke sath
        local_supply_with_bat, grid_imp = get_reactive_action(solar, demand, battery)
        f_with = freq_with_battery.update(local_supply_with_bat, demand)
        
        data.append({
            "hour": step,
            "f_no_bat": f_no,
            "f_with_bat": f_with
        })
        
    df = pd.DataFrame(data)
    
    # Check violations (Blackout risk jab frequency < 49.5 ya > 50.5 ho)
    violation_no = len(df[(df["f_no_bat"] < 49.5) | (df["f_no_bat"] > 50.5)])
    violation_with = len(df[(df["f_with_bat"] < 49.5) | (df["f_with_bat"] > 50.5)])
    
    print("=== RESULTS ===")
    print(f"Danger Hours (Bina Battery): {violation_no} hours")
    print(f"Danger Hours (Smart Battery): {violation_with} hours")
    
    # Graph Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df["hour"], df["f_no_bat"], label="Frequency (NO Battery)", color="red", linewidth=2)
    plt.plot(df["hour"], df["f_with_bat"], label="Frequency (WITH Battery)", color="blue", linestyle="--", linewidth=2)
    plt.axhline(50.0, color='green', label="Ideal (50 Hz)", linewidth=1)
    plt.axhline(49.5, color='orange', linestyle=':', label="Blackout Limit")
    plt.title("Grid Frequency (Heartbeat): No Battery vs Reactive Controller")
    plt.xlabel("Total Hours")
    plt.ylabel("Frequency (Hz)")
    plt.legend()
    plt.grid(True)
    
    os.makedirs(os.path.join(os.path.dirname(__file__), "../data"), exist_ok=True)
    save_path = os.path.join(os.path.dirname(__file__), "../data/frequency_graph.png")
    plt.savefig(save_path)
    print(f"Graph saved at: {save_path}")

if __name__ == "__main__":
    run_comparison()