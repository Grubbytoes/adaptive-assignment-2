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
        self.vision = []
        self.move_dir = vector2.rand()
        self.nest = nest
        self.state = Critter.WANDER
        
        # flower seeking logic
        self.possible_flower: FlowerData = None
        self.confirmed_flower = None
        
        # private/hidden members
        self._neighboring_critters = (-1, [])
    def step(self):
        super().step()
        
        
        # fill vision
        self.vision.clear()
        self.vision.extend(self.get_field_neighbors(self.sight_range))
    
        # state behaviour
        if self.state == Critter.WANDER:
            self.wander()
        elif self.state == Critter.COLLECTING:
            self.collecting()
        elif self.state == Critter.HOMING:
            self.homing()
        elif self.state == Critter.SEEKING:
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
           
        # Are there any flowers in our field of vision?
        f = self.check_for_flowers()
        if f != None:
            self.confirmed_flower = f
            self.state = Critter.COLLECTING
                
    # Used when a critter is attracted to that flower. Will take nectar and begin homing once flower has been reached
    # until then will move towards flower
    def collecting(self):
        # check that the flower still exists in space - ie has not been exhausted
        if 1 > self.confirmed_flower.nectar or self.confirmed_flower.pos is None:
            self.state = Critter.WANDER
            self.confirmed_flower = None
            return
        
        if self.is_touching(self.confirmed_flower):
            self.take_and_log_nectar(self.confirmed_flower)
            self.state = Critter.HOMING
            return
        
        self.move_towards(self.confirmed_flower.pos)
    
    # The critter is moving towards a flower that it thinks exists in space
    # it will enter the collecting state one it reaches it, or if it encounters another flower
    # along the way
    # it will enter the wandering state if it arrives at the position and there is no flower
    def seeking(self):
        self.move_towards(self.possible_flower.pos)
        
        # look for flowers
        f = self.check_for_flowers()
        if f != None:
            self.confirmed_flower = f
            self.state = Critter.COLLECTING
        
        # give up if we've reached that position without finding anything
        distance = self.distance(self.possible_flower.pos)
        if self.sight_range/2 > distance:
            self.possible_flower = None
            self.state = Critter.WANDER

    # Critter will move towards the nest, and deposit nectar
    # then will pick a random direction and enter the wandering state
    def homing(self):
        if self.is_touching(self.nest):
            self.nest.deposit_nectar()            
            self.state = Critter.WANDER
            self.move_dir = vector2.rand()
            return
        
        self.move_towards(self.nest.pos)
    
    # Incorporates separation steer of boid like behaviour into move_dir 
    # defined as the sum of the negative relative distances to all nearby critters
    def separation(self, weight):
        steer = np.zeros(2)
        for other in self.get_neighboring_critters():
            steer = np.add(steer, np.negative(self.relative_position_of(other)))
        
        if weight != 1:
            steer = np.multiply(steer, weight)
        
        self.move_dir = np.add(steer, self.move_dir)
    
    # Incorporates alignment
    # defined as the mean of the movement directions of all nearby critters
    def alignment(self, weight):
        _test = self.get_neighboring_critters()
        directions = np.array([
            other.move_dir
            for other
            in _test
        ])
        
        if 0 >= len(directions):
            return
        
        steer = np.mean(directions, 0)

        if weight != 1:
            steer = np.multiply(steer, weight)

        self.move_dir = np.add(steer, self.move_dir)
    
    # Incorporates cohesion
    # defined as the mean position of all nearby critters
    def cohesion(self, weight):
        positions = np.array([
            self.relative_position_of(other)
            for other
            in self.get_neighboring_critters()
        ])
        
        if 0 >= len(positions):
            return
        
        steer = np.mean(positions, 0)

        if weight != 1:
            steer = np.multiply(steer, weight)
        
        self.move_dir = np.add(steer, self.move_dir)
    
    # look for flowers in the Critters vision
    # if one is found, return it
    def check_for_flowers(self):
        for n in self.vision:
            if n.type == "flower":
                return n
            
        return None
    
    # take nectar from a flower, and log its position if there is still any menkar remaining
    def take_and_log_nectar(self, flower):
        flower.take_nectar()
        if 0 < flower.nectar:
            self.log_flower(flower.pos, flower.nectar)
        else:
            self.possible_flower = None
    
    # Set the critters move_dir towards a position in space (normalizes by default)
    def move_towards(self, point, normalize=True):
        if normalize:
            self.move_dir = vector2.normalized(self.relative_position(point))
        else:
            self.move_dir = self.relative_position(point)
    
    # Log a position in space where we believe/remember a flower to be, along with how much nectar it's meant to have
    def log_flower(self, p, n):
        self.possible_flower = FlowerData(
            pos=p,
            nectar=n
        )
    
    def get_neighboring_critters(self):
        if self._neighboring_critters[0] == self.step_count:
            return self._neighboring_critters[1]
        else:
            self._neighboring_critters = (
                self.step_count,
                [n for n in self.vision if n.type == "critter"]
            )
            return self._neighboring_critters[1]


@dataclass
class FlowerData:
    pos: tuple
    nectar: int    


def turning_noise(v):
    return vector2.rotated(v, np.random.randint(-2, 3))