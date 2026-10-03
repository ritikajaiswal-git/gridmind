import sys
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.solar import get_solar_kw
from simulator.demand import get_demand_kw
from simulator.battery import Battery
from reactive import get_reactive_action
from forecast_aware import get_smart_action

def run_comparison(days=3):
    bat_reactive = Battery(capacity=100.0, max_power=50.0)
    bat_smart = Battery(capacity=100.0, max_power=50.0)
    
    reactive_peak_grid = 0
    smart_peak_grid = 0
    
    for step in range(days * 24):
        hour = step % 24
        solar = get_solar_kw(hour)
        demand = get_demand_kw(hour)
        
        # 1. Purana Bevkuf Controller
        _, grid_react = get_reactive_action(solar, demand, bat_reactive)
        
        # 2. Naya Smart AI Controller
        _, grid_smart, reason = get_smart_action(hour, solar, demand, bat_smart)
        
        # HUME SIRF PEAK HOURS (18:00 - 22:00) SE MATLAB HAI
        if 18 <= hour <= 22:
            reactive_peak_grid += grid_react
            smart_peak_grid += grid_smart
            
    reduction = ((reactive_peak_grid - smart_peak_grid) / reactive_peak_grid) * 100
    
    # Save Metrics for Dashboard
    metrics = {
        "reactive_peak_kwh": round(reactive_peak_grid, 2),
        "smart_peak_kwh": round(smart_peak_grid, 2),
        "reduction_percent": round(reduction, 1)
    }
    
    data_dir = os.path.join(os.path.dirname(__file__), "../data")
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f)
        
    print("=== CONTROLLER COMPARISON (3 DAYS) ===")
    print(f"Reactive (Old) Peak Grid Import : {metrics['reactive_peak_kwh']} kWh")
    print(f"Smart (AI) Peak Grid Import     : {metrics['smart_peak_kwh']} kWh")
    print(f"Total Saving in Peak Load       : {metrics['reduction_percent']}% !!!")
    
    # Barchart banana
    plt.figure(figsize=(8, 5))
    bars = plt.bar(["Reactive Controller", "Smart AI Controller"], 
                   [reactive_peak_grid, smart_peak_grid], 
                   color=['red', 'blue'])
    plt.title("Total Grid Import During Evening Peak (Lower is Better)")
    plt.ylabel("kWh Imported from Grid")
    
    save_path = os.path.join(data_dir, "compare_graph.png")
    plt.savefig(save_path)
    print(f"Graph saved at: {save_path}")

if __name__ == "__main__":
    run_comparison()