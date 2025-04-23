import numpy as np

from mymathstuff import vector2
from .field_agent import FieldAgent

class Critter(FieldAgent):
    colour = "gold"
    type = "critter"

    def __init__(self, model, nest, sight_range=10):
        super().__init__(model)
        
        self.sight_range = max(sight_range, 1)
        self.move_dir = vector2.rand()
        self.nest = nest
        
    def step(self):
        super().step()
        
        # looking for flowers
        for n in self.get_field_neighbors(8):
            if n.type == "flower":
                #! PURELY FOR DEMONSTRATION
                n.kill()
        
        self.wander()
        
        # normalize, and turning noise, and move
        self.move_dir = turning_noise(vector2.normalized(self.move_dir))
        self.move(*self.move_dir)

    def wander(self):
        # TODO improve this
        pass


def turning_noise(v):
    return vector2.rotated(v, np.random.randint(-2, 3))