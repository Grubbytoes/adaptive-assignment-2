import random

from swarm_critters import *
from math import pow, sqrt

# The job of this script is to take a newly instanced field and fill it with agents (nest, flowers, critters) in such a way
# that is conducive to the rest of our experiment

class EnvironmentManager:
    def __init__(self, field):
        self.field: Field = field
        self.is_initialized = False
    
    def initialize(self, critter_count=8, flower_count=24, minimum_flower_distance=10):
        if self.is_initialized:
            print(f"WARNING: {self} is already initialized")
            return
        
        # 1. place the nest in the center
        nest = Nest(self.field)
        self.field.place_agent(
            nest,
            int(self.field.width / 2),
            int(self.field.height / 2),
        )
        
        # 2. generate critters around the nest
        nest_neighbourhood = list(self.field.space.get_neighborhood(
            nest.pos,
            False, 
            False,
            int(sqrt(critter_count))*2
        ))
        random.shuffle(nest_neighbourhood)
        for pos, i in zip(nest_neighbourhood, range(critter_count)):
            new_critter = Critter(self.field, nest)
            self.field.place_agent(new_critter, *pos)
        
        # 3. generate flowers
        for i in range(flower_count):
            new_flower = Flower(self.field)
            flower_position = self.random_position()
            self.field.place_agent(new_flower, *flower_position)
    
    def random_position(self, only_if_empty=True):
        pos = (
            random.randint(0, self.field.width-1),
            random.randint(0, self.field.height-1),
        )
        
        while only_if_empty and not self.field.space.is_cell_empty(pos):
            pos = (
                random.randint(0, self.field.width-1),
                random.randint(0, self.field.height-1),
            )

        return pos
    
    def get_critters(self):
        return self.field.agents_by_type(Critter)
    
    def get_flowers(self):
        return self.field.agents_by_type(Flower)
    
    def get_nest(self):
        return self.field.agents_by_type(Nest)[0]