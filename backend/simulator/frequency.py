class GridFrequency:
    def __init__(self, nominal=50.0):
        self.nominal = nominal
        self.current = nominal

    def update(self, local_supply_kw, demand_kw):
        # Mismatch: Humare paas kitni bijli hai vs kitni chahiye
        net_power = local_supply_kw - demand_kw
        
        # Simple formula: 1 kW ki kami se frequency 0.01 Hz gir jati hai
        deviation = net_power * 0.01
        
        # Nayi frequency update karo
        self.current = self.nominal + deviation
        
        # Real life mein system fail ho jata hai, par hum isko 48.0 se 52.0 ke beech rok lenge
        self.current = max(48.0, min(52.0, self.current))
        return self.current