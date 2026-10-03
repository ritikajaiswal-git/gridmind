import sys
import os
import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simulator.solar import get_solar_kw
from simulator.demand import get_demand_kw
from simulator.battery import Battery
from controller.forecast_aware import get_smart_action
from controller.reactive import get_reactive_action # NAYA: Purana bevkuf controller
from carbon.ledger import verify_ledger, add_record

app = FastAPI(title="GridMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GridState:
    def __init__(self):
        self.step = 0
        self.battery = Battery(capacity=100.0, max_power=50.0)
        self.current_data = {}
        self.ai_enabled = True # NAYA: AI by default ON hai

state = GridState()

# NAYA: Frontend se Switch ON/OFF ka signal lene ke liye
class ToggleRequest(BaseModel):
    ai_enabled: bool

@app.post("/toggle-ai")
def toggle_ai(req: ToggleRequest):
    state.ai_enabled = req.ai_enabled
    return {"status": "success", "ai_enabled": state.ai_enabled}

async def run_simulation_loop():
    while True:
        hour = state.step % 24
        solar = get_solar_kw(hour)
        demand = get_demand_kw(hour)
        
        # NAYA: Agar AI ON hai toh Smart Action, warna purana Reactive action
        if state.ai_enabled:
            local_supply, grid_import, reason = get_smart_action(hour, solar, demand, state.battery)
        else:
            local_supply, grid_import = get_reactive_action(solar, demand, state.battery)
            reason = "🔴 AI DISABLED: Using old reactive rules (No future planning!)"
            
        if solar > 0 or grid_import > 0:
            add_record("GridMind-AI", solar_kwh=solar, grid_kwh=grid_import)
            
        state.current_data = {
            "hour": f"{hour:02d}:00",
            "solar_kw": round(solar, 2),
            "demand_kw": round(demand, 2),
            "battery_soc": round(state.battery.soc_kwh, 2),
            "grid_import_kw": round(grid_import, 2),
            "action_reason": reason,
            "ai_enabled": state.ai_enabled
        }
        
        state.step += 1
        await asyncio.sleep(2.0)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_simulation_loop())

@app.get("/telemetry")
def get_telemetry():
    return state.current_data

@app.get("/ledger")
def get_ledger_data():
    ledger_path = os.path.join(os.path.dirname(__file__), "../data/ledger.jsonl")
    records = []
    if os.path.exists(ledger_path):
        with open(ledger_path, 'r') as f:
            for line in f.readlines()[-5:]:
                records.append(json.loads(line))
    return records