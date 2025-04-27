import mesa

from .field_agent import FieldAgent

class Nest(FieldAgent):
    colour = "firebrick1"
    type = "nest"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nectar = 0
    
    def deposit_nectar(self):
        # Takes nectar deposited by a critter
        self.nectar += 1
        print(self.nectar)