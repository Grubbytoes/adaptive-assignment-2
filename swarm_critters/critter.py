import numpy as np

from .field_agent import FieldAgent

class Critter(FieldAgent):
    colour = "gold"

    def __init__(self, model, nest, sight_range=10):
        super().__init__(model)
        
        self.sight_range = max(sight_range, 1)
        self.velocity = np.zeros(2)
        self.nest = nest
        
    def step(self):
        super().step()
        print(f"{self.unique_id} - beep")

    def do_move(self):
        raise NotImplementedError("Critters cannot move yet!!")

