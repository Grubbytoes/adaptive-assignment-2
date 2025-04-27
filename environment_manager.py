import random
import json

from swarm_critters import *
from math import pow, sqrt

# The job of this script is to take a newly instanced field and fill it with agents (nest, flowers, critters) in such a way
# that is conducive to the rest of our experiment

class EnvironmentManager:
    def __init__(self, field):
        self.field: Field = field
        self.is_initialized = False
        
        self.flower_frequency = None
        self.flower_richness = None
    
    def initialize(self, critter_count=8, flower_frequency=0.2, flower_richness=5):
        self.flower_frequency = flower_frequency
        self.flower_richness = flower_richness
        
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
        max_nest_distance = int(sqrt(critter_count))
        for i in range(critter_count):
            pos = (
                random.randint(nest.pos[0] - max_nest_distance, nest.pos[0] + max_nest_distance),
                random.randint(nest.pos[1] - max_nest_distance, nest.pos[1] + max_nest_distance)
            )
            new_critter = Critter(self.field, nest)
            self.field.place_agent(new_critter, *pos)
        
        # 3. generate flowers
        total_field_area = self.field.width * self.field.height
        for i in range(int(total_field_area * flower_frequency / 50)):
            new_flower = Flower(self.field, flower_richness)
            flower_position = self.random_position()
            self.field.place_agent(new_flower, *flower_position)
        
        self.is_initialized = True
    
    def run(self, cycle_length, cycles, field_callback = None):
        if not self.is_initialized:
            return
        
        self.get_nest().cycle_length = cycle_length
        self.field.run_for(cycles * cycle_length, field_callback)
        
    def random_position(self):
        pos = (
            random.randint(0, self.field.width-1),
            random.randint(0, self.field.height-1),
        )

        return pos
    
    def get_critters(self):
        return self.field.agents_by_type(Critter)
    
    def get_flowers(self):
        return self.field.agents_by_type(Flower)
    
    def get_nest(self) -> Nest:
        return self.field.agents_by_type[Nest][0]
    
    def dump(self):
        return json.dumps(
            {
                "flower frequency": self.flower_frequency,
                "flower richness": self.flower_richness,
                "nectar per cycle": self.get_nest().nectar_per_cycle
            }
        )