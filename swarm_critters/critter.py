import numpy as np

from mymathstuff import vector2
from .field_agent import FieldAgent
from .flower import Flower

class Critter(FieldAgent):
    colour = "gold"
    type = "critter"
    
    WANDER = 0
    ATTRACTED = 1
    HOMING = 2

    def __init__(self, model, nest, sight_range=5):
        super().__init__(model)
        
        self.sight_range = max(sight_range, 1)
        self.move_dir = vector2.rand()
        self.nest = nest
        self.target_flower = None
        self.state = self.WANDER
        
    def step(self):
        super().step()
        
        if self.state == self.WANDER:
            self.wander()
        if self.state == self.ATTRACTED:
            self.attracted(self.target_flower)
        if self.state == self.HOMING:
            self.homing()
                
        # normalize, and turning noise, and move
        self.move_dir = turning_noise(vector2.normalized(self.move_dir))
        self.move(*self.move_dir)

    def wander(self):
        # search for flowers
        neighbors = self.get_field_neighbors(self.sight_range)
        
        for n in neighbors:
            if n.type != "flower":
                continue
            self.target_flower = n
            self.state = self.ATTRACTED
                

    def attracted(self, flower: Flower):
        # Used when a critter is attracted to that flower. Will take pollen and begin homing once flower has been reached
        # until then will move towards flower
        if self.is_touching(flower):
            flower.take_pollen()
            self.state = self.HOMING
            return
        
        self.move_towards(flower)
        

    def homing(self):
        # Critter will move towards the nest, and deposit pollen
        # then will pick a random direction and enter the wandering state
        if self.is_touching(self.nest):
            self.nest.deposit_pollen()
            self.state = self.WANDER
            self.move_dir = vector2.rand()
            return
        
        self.move_towards(self.nest)
    
    def move_towards(self, other: FieldAgent, normalize=True):
        if normalize:
            self.move_dir = vector2.normalized(self.relative_position_of(other))
        else:
            self.move_dir = self.relative_position_of(other)



def turning_noise(v):
    return vector2.rotated(v, np.random.randint(-2, 3))