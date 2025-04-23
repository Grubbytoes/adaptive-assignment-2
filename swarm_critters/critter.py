import numpy as np
import mymathstuff

from .field_agent import FieldAgent

class Critter(FieldAgent):
    colour = "gold"

    def __init__(self, model, nest, sight_range=10):
        super().__init__(model)
        
        self.sight_range = max(sight_range, 1)
        self.velocity = random_velocity()
        self.nest = nest
        self.pos_from_nest = [0, 0]
        self.boid_radius = 5
        
    def step(self):
        super().step()
        
        # move by our current velocity
        self.velocity = self.move_by_velocity()

    def move_by_velocity(self):
        # moves by, and returns, velocity normalized
        v_normalized = mymathstuff.vec2_normalized(self.velocity)
        self.move(*v_normalized)
        return v_normalized
    
    def place(self, space, x=0, y=0):
        super().place(space, x, y)
        self.pos_from_nest = [
            self.nest.pos[0] + x,
            self.nest.pos[1] + y
        ]

def random_velocity():
    coords = [0, 100]
    coords = mymathstuff.vec2_rotated(coords, np.random.randint(0, 360))
    return np.array(coords)