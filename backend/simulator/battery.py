class Battery:
    def __init__(self, capacity=100.0, max_power=50.0, efficiency=0.9):
        self.capacity = capacity
        self.max_power = max_power
        self.efficiency = efficiency
        # Shuru mein battery aadhi (50%) bhari hai
        self.soc_kwh = capacity * 0.5 

    def charge(self, kw, hours=1):
        # Battery apni max_power limit se zyada speed se charge nahi ho sakti
        power_in = min(kw, self.max_power)
        energy_added = power_in * hours * self.efficiency
        
        # Tank (capacity) full hone ke baad overcharge nahi kar sakte
        self.soc_kwh = min(self.capacity, self.soc_kwh + energy_added)
        return power_in

    def discharge(self, kw, hours=1):
        power_out = min(kw, self.max_power)
        energy_needed = power_out * hours
        
        # Check karte hain ki utni power battery mein bachi hai ya nahi
        if self.soc_kwh >= energy_needed:
            self.soc_kwh -= energy_needed
            return power_out
        else:
            # Agar kam bachi hai, toh jitni bachi hai utni hi de do
            actual_power = self.soc_kwh / hours
            self.soc_kwh = 0.0
            return actual_power