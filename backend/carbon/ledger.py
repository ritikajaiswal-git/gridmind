import os
import json
import hashlib
from datetime import datetime

# Ledger file ka address
LEDGER_FILE = os.path.join(os.path.dirname(__file__), "../data/ledger.jsonl")

def calculate_hash(record):
    # Data ko ek string mein badal kar uska secret hash code banata hai
    record_string = f"{record['timestamp']}{record['building']}{record['solar_kwh']}{record['grid_kwh']}{record['avoided_kg_co2']}{record['prev_hash']}"
    return hashlib.sha256(record_string.encode('utf-8')).hexdigest()

def add_record(building_name, solar_kwh, grid_kwh, emission_factor=0.71):
    # CO2 bachaya = Jitni dhoop use ki * Grid ka pollution rate
    avoided_co2 = round(solar_kwh * emission_factor, 2)
    
    # Pichla hash nikalo (Chain jodne ke liye)
    prev_hash = "0000" # Default (agar file khali hai)
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'r') as f:
            lines = f.readlines()
            if lines:
                last_record = json.loads(lines[-1])
                prev_hash = last_record['hash']
                
    # Naya record banao
    new_record = {
        "timestamp": datetime.now().isoformat(),
        "building": building_name,
        "solar_kwh": round(solar_kwh, 2),
        "grid_kwh": round(grid_kwh, 2),
        "avoided_kg_co2": avoided_co2,
        "prev_hash": prev_hash
    }
    
    # Is record ka naya hash bana kar record mein daal do
    new_record['hash'] = calculate_hash(new_record)
    
    # File mein nayi line jod do (Append mode 'a')
    with open(LEDGER_FILE, 'a') as f:
        f.write(json.dumps(new_record) + "\n")
        
    return new_record

def verify_ledger():
    if not os.path.exists(LEDGER_FILE):
        return {"valid": True, "message": "Ledger is empty"}
        
    with open(LEDGER_FILE, 'r') as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        record = json.loads(lines[i])
        
        # 1. Check karo kya usne CO2 values ke sath fraud kiya hai?
        expected_co2 = round(record['solar_kwh'] * 0.71, 2)
        if record['avoided_kg_co2'] != expected_co2:
            return {"valid": False, "broken_index": i, "reason": "CO2 calculation tampered!"}
            
        # 2. Check karo kya Hash Chain sahi hai?
        stored_hash = record['hash']
        calculated_hash = calculate_hash(record)
        
        if stored_hash != calculated_hash:
            return {"valid": False, "broken_index": i, "reason": "Hash signature broken!"}
            
        # 3. Check pichla link
        if i > 0:
            prev_record = json.loads(lines[i-1])
            if record['prev_hash'] != prev_record['hash']:
                return {"valid": False, "broken_index": i, "reason": "Chain link broken!"}
                
    return {"valid": True, "message": "All records are 100% authentic."}

# Test karne ke liye ek chhota sa script
if __name__ == "__main__":
    print("Testing Carbon Ledger...")
    # Delete old test ledger if exists
    if os.path.exists(LEDGER_FILE):
        os.remove(LEDGER_FILE)
        
    add_record("Hospital", solar_kwh=50.0, grid_kwh=10.0)
    add_record("School", solar_kwh=30.0, grid_kwh=5.0)
    
    result = verify_ledger()
    print(f"Status after adding valid records: {result}")