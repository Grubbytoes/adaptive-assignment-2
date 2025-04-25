import numpy as np

from dataclasses import dataclass
from mymathstuff import vector2
from .field_agent import FieldAgent

class Critter(FieldAgent):
    colour = "gold"
    type = "critter"
    
    WANDER = 0
    COLLECTING = 1
    HOMING = 2
    SEEKING = 3

    def __init__(self, model, nest, sight_range=5):
        super().__init__(model)
        
        self.sight_range = max(sight_range, 1)
        self.move_dir = vector2.rand()
        self.nest = nest
        self.state = Critter.WANDER
        
        # flower seeking logic
        self.possible_flower: FlowerData = None
        self.confirmed_flower = None
        
    def step(self):
        super().step()
        
        if self.state == Critter.WANDER:
            self.wander()
        if self.state == Critter.COLLECTING:
            self.collecting(self.confirmed_flower)
        if self.state == Critter.HOMING:
            self.homing()
        if self.state == Critter.SEEKING:
            self.seeking()
                
        # normalize, and turning noise, and move
        self.move_dir = turning_noise(vector2.normalized(self.move_dir))
        self.move(*self.move_dir)

    # critter wanders along a straight line, searching for flowers
    def wander(self):
        # do we know where any flowers are?
        if self.possible_flower != None:
            self.state = Critter.SEEKING
            return
        
        neighbors = self.get_field_neighbors(self.sight_range)
        self.look_for_flowers(neighbors)
                
    # Used when a critter is attracted to that flower. Will take nectar and begin homing once flower has been reached
    # until then will move towards flower
    def collecting(self, flower):
        # check that the flower still exists in space - ie has not been exhausted
        if 1 > flower.nectar or flower.pos is None:
            self.state = Critter.WANDER
            self.confirmed_flower = None
            return
        
        if self.is_touching(flower):
            self.take_and_log_nectar(flower)
            self.state = Critter.HOMING
            return
        
        self.move_towards(flower)
    
    # The critter is moving towards a flower that it thinks exists in space
    # it will enter the collecting state one it reaches it, or if it encounters another flower
    # along the way
    # it will enter the wandering state if it arrives at the position and there is no flower
    def seeking(self):
        raise NotImplementedError("seeking behaviour not implemented")

    # Critter will move towards the nest, and deposit nectar
    # then will pick a random direction and enter the wandering state
    def homing(self):
        if self.is_touching(self.nest):
            self.nest.deposit_nectar()            
            self.state = Critter.WANDER
            self.move_dir = vector2.rand()
            return
        
        self.move_towards(self.nest)
    
    # Take a set/list of flowers (ie one that has been gathered from the neighborhood) and look for flowers
    # if one is found, move to collect nectar
    def look_for_flowers(self, neighbors):
        for n in neighbors:
            if n.type != "flower":
                continue
            self.confirmed_flower = n
            self.state = Critter.COLLECTING
    
    # take nectar from a flower, and log its position if there is still any menkar remaining
    def take_and_log_nectar(self, flower):
        flower.take_nectar()
        if 0 < flower.nectar:
            self.log_flower(flower.pos, flower.nectar)
        else:
            self.possible_flower = None
    
    # Set the critters move_dir towards a position in space (normalizes by default)
    def move_towards(self, other: FieldAgent, normalize=True):
        if normalize:
            self.move_dir = vector2.normalized(self.relative_position_of(other))
        else:
            self.move_dir = self.relative_position_of(other)
    
    # Log a position in space where we believe/remember a flower to be, along with how much nectar it's meant to have
    def log_flower(self, p, n):
        self.possible_flower = FlowerData(
            pos=p,
            nectar=n
        )

@dataclass
class FlowerData:
    pos: tuple
    nectar: int    


def turning_noise(v):
    return vector2.rotated(v, np.random.randint(-2, 3))