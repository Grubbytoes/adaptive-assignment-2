import numpy as np

from dataclasses import dataclass
from mymathstuff import vector2
from .field_agent import FieldAgent

class Critter(FieldAgent):
    colour = "gold"
    type = "critter"
    base_confidence = 10
    searching_turn_angle = 60
    
    SEARCHING = 's'
    HOMING = 'h'

    def __init__(self, model, nest, sight_range=5):
        super().__init__(model)
        
        self.sight_range = max(sight_range, 1)
        self.vision = []
        self.move_dir = vector2.rand()
        self.nest = nest
        self.state = Critter.SEARCHING
        
        # Hugo's algorithm
        self.confidence = 0
        self.clock = 0

    def step(self):
        super().step()
        
        # fill vision
        self.vision.clear()
        self.vision.extend(self.field_neighbors(self.sight_range))
    
        # state behaviour
        if self.state == Critter.HOMING:
            self.homing()
        elif self.state == Critter.SEARCHING:
            self.searching()
        else:
            # if we've somehow entered a bad state, return to the searching state
            self.state = Critter.SEARCHING
                
        # normalize, and turning noise, and move
        self.move_dir = random_turn(vector2.normalized(self.move_dir))
        self.move(*self.move_dir)

    # critter wanders along a straight line, searching for flowers
    def searching(self):                  
        other_flower = None # the closest flower
        other_critters = [] # all neighboring critters
        
        for other in self.vision:
            if other.type == "flower":
                # we only care if this is the only flower, or the closest one
                if (
                    other_flower != None and
                    self.distance(other_flower.pos) < self.distance(other.pos)
                ): continue
                other_flower = other
            elif other.type == "critter":
                other_critters.append(other)
        
        # flower seeking logic
        if other_flower != None and self.is_touching(other_flower):
            self.state = Critter.HOMING
            # TODO needs testing this is ROUGH CODE ONLY
            self.clock = 0
            self.state = Critter.HOMING
            other_flower.take_nectar()            
        elif other_flower != None:
            self.confidence = 1
            self.move_towards(other_flower.pos)
        
        # TODO critter communication
        
        # base
        self.confidence = max(0, self.confidence - 1)
        if self.confidence == 0:
            self.confidence = Critter.base_confidence
            self.move_dir = random_turn(self.move_dir, Critter.searching_turn_angle)           
        

    # Critter will move towards the nest, and deposit nectar
    # then will pick a random direction and enter the wandering state
    def homing(self):
        # TODO refine this is ROUGH CODE ONLY
        if self.is_touching(self.nest):
            self.nest.deposit_nectar(self, time=self.clock)            
            self.state = Critter.SEARCHING
            self.move_dir = np.multiply(self.move_dir, -1)
            self.confidence = self.clock
        else:
            self.move_towards(self.nest.pos)
            self.clock += 1
    
    # Incorporates separation steer of boid like behaviour into move_dir 
    # defined as the sum of the negative relative distances to all nearby critters
    def separation(self, others, weight=1):
        steer = np.zeros(2)
        for other in others:
            steer = np.add(steer, np.negative(self.relative_position(other.pos)))
        
        if weight != 1:
            steer = np.multiply(steer, weight)
        
        self.move_dir = np.add(steer, self.move_dir)
    
    # Incorporates alignment
    # defined as the mean of the movement directions of all nearby critters
    def alignment(self, others, weight=1):
        directions = np.array([
            other.move_dir
            for other
            in others
        ])
        
        if 0 >= len(directions):
            return
        
        steer = np.mean(directions, 0)

        if weight != 1:
            steer = np.multiply(steer, weight)

        self.move_dir = np.add(steer, self.move_dir)
    
    # Incorporates cohesion
    # defined as the mean position of all nearby critters
    def cohesion(self, others, weight=1):
        positions = np.array([
            self.relative_position(other.pos)
            for other
            in others
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
    
    # take nectar from a flower, and log its position if there is still any nectar remaining
    def take_and_log_nectar(self, flower):
        self.last_flower_found_at = self.step_count
        
        flower.take_nectar()
        if 0 < flower.nectar:
            self.log_flower(flower.pos, flower.nectar)
        else:
            self.possible_flower = None
    
    # Log a position in space where we believe/remember a flower to be, along with how much nectar it's meant to have
    def log_flower(self, p, n):
        self.possible_flower = FlowerData(
            pos=p,
            nectar=n
        )
    
    # Returns how recently the other has visited a flower, compared to the self
    # Will be positive if the other has visited a flower MORE recently, otherwise negative
    def compare(self, other):
        return other.last_flower_found_at - self.last_flower_found_at
        

@dataclass
class FlowerData:
    pos: tuple
    nectar: int    


def random_turn(v, amount=1):
    return vector2.rotated(v, np.random.randint(-amount, amount+1))