import random
import json

from swarm_critters import *
from math import pow, sqrt

RESULTS_FOLDER = "results"
INITIAL_FLOWER_F = 2
INITIAL_FLOWER_R = 5

# The job of this script is to take a newly instanced field and fill it with agents (nest, flowers, critters) in such a way
# that is conducive to the rest of our experiment

class EnvironmentManager:
    def __init__(self, field):
        self.field: Field = field
        self.is_initialized = False
    
    def initialize(self, critter_count=8, social_critters=True):
       
        if self.is_initialized:
            print(f"WARNING: {self} is already initialized")
            return
        
        # 1. place the nest in the center
        nest = Nest(self.field)
        self.field.place_agent(
            nest,
            int(self.field.size() / 2),
            int(self.field.size() / 2),
        )
        
        # 2. generate critters around the nest
        max_nest_distance = int(sqrt(critter_count))
        new_critter: Critter
        for i in range(critter_count):
            pos = (
                random.randint(nest.pos[0] - max_nest_distance, nest.pos[0] + max_nest_distance),
                random.randint(nest.pos[1] - max_nest_distance, nest.pos[1] + max_nest_distance)
            )
            
            if social_critters:
                new_critter = SocialCritter(self.field, nest)
            else:
                new_critter = Critter(self.field, nest)
            
            self.field.place_agent(new_critter, *pos)
        
        # 3. generate flowers
        self.field.set_flower_population(
            INITIAL_FLOWER_F,
            INITIAL_FLOWER_R
        )
        
        self.is_initialized = True
    
    def run_environment(self, cycle_length, cycles, field_callback = None):
        if not self.is_initialized:
            return
        
        self.get_nest().cycle_length = cycle_length
        self.field.run_for(cycles * cycle_length, field_callback)
    
    def get_critters(self):
        return self.field.agents_by_type(Critter)
    
    def get_flowers(self):
        return self.field.agents_by_type(Flower)
    
    def get_nest(self) -> Nest:
        return self.field.agents_by_type[Nest][0]
    
    def save_dump(self, file_name):
        file = open(f"{RESULTS_FOLDER}/{file_name}", 'w')
        return json.dump(
            {
                "flower frequency": self.flower_frequency,
                "flower richness": self.flower_richness,
                "nectar per cycle": self.get_nest().nectar_per_cycle
            },
            file
        )