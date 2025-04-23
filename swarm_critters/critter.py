import numpy as np

from .field_agent import FieldAgent

class Critter(FieldAgent):
    colour = "gold"

    def __init__(self, model, nest, sight_range=10):
        super().__init__(model)
        
        self.sight_range = max(sight_range, 1)
        self.velocity = np.array(random_initial_velocity())
        self.nest = nest
        
    def step(self):
        super().step()
        self.move_by_velocity()

    def move_by_velocity(self):
        self.move(*self.velocity)

def random_initial_velocity():
    coords = [0, 0]
    
    for i in range(2):
        coords[np.random.randint(0,2)] += 1
        
    for i in range(2):
        if np.random.randint(0,2) == 1:
            coords[i] *= -1
    
    return coords