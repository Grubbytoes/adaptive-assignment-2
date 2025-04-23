import numpy as np

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
        
        #! probably better to do this in something more memory efficient than a string
        self.state = "explore"
        
    def step(self):
        super().step()
        
        # move by our current velocity
        self.move_by_velocity()
        
        # start calculating our current velocity
        self.velocity = random_velocity()

    def move_by_velocity(self):
        normalized_v = [0, 0]
        
        for i in range(2):
            normalized_v[i] = max(-1, min(self.velocity[i], 1))
        
        self.move(*normalized_v)
    
    def move(self, x, y):
        super().move(x, y)
        self.pos_from_nest[0] += x
        self.pos_from_nest[1] += y
    
    def place(self, space, x=0, y=0):
        super().place(space, x, y)
        self.pos_from_nest = [
            self.nest.pos[0] + x,
            self.nest.pos[1] + y
        ]

def random_velocity():
    coords = [0, 0]
    coords[np.random.randint(0, 2)] = np.random.choice((-1, 1))
    return np.array(coords)