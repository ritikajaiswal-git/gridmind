# Modbus registers ek locker ki tarah hain jahan live data rakha jata hai
REGISTERS = {
    40001: 0.0,  # Solar Power (kW)
    40002: 0.0,  # Demand Power (kW)
    40003: 0.0,  # Battery SoC (kWh) - SoC ka matlab State of Charge
    40004: 0.0,  # Grid Import (kW) - Govt grid se kitni li
    40005: 50.0  # Frequency (Hz)
}

def write_register(address, value):
    REGISTERS[address] = round(value, 2)

def read_register(address):
    return REGISTERS.get(address, 0.0)