import mesa

from .field_agent import FieldAgent

class Nest(FieldAgent):
    colour = "firebrick1"
    type = "nest"
    
    def __init__(self, *args, cycle_length = 365, **kwargs):
        super().__init__(*args, **kwargs)
        self.nectar = 0
        self.cycle_length = cycle_length
        self.nectar_per_cycle = []
    
    def step(self):
        super().step()
    
        if self.step_count % self.cycle_length == self.cycle_length-1:
            self.nectar_per_cycle.append(self.nectar)
            print(self.nectar_per_cycle)
            
    
    def deposit_nectar(self):
        # Takes nectar deposited by a critter
        self.nectar += 1