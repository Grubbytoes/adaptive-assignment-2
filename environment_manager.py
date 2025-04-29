import random
import json

from swarm_critters import *
from math import pow, sqrt

RESULTS_FOLDER = "results"
CYCLE_LENGTH = 100
SEASON_LENGTH = 30
SEASON_PARAMS = (
    (1.5, 10), # SPRING
    (2, 6), # SUMMER
    (1.5, 6), # AUTUMN
    (.5, 25) # WINTER
)

# This script runs the experiment with a single set of parameters

class EnvironmentManager:
    def __init__(self, size, critter_count=8, social_critters=False):
        self.field: Field = Field(size)
        self.is_initialized = False
        self.social_critters = social_critters
        
        self.initialize(critter_count, social_critters)
    
    def initialize(self, critter_count=8, social_critters=True):
       
        if self.is_initialized:
            print(f"WARNING: {self} is already initialized")
            return
        
        # 1. place the nest in the center
        nest = Nest(self.field, cycle_length=CYCLE_LENGTH, pheromone_queue_len=12)
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
        
        # Ready to go!
        self.is_initialized = True
    
    def run_environment(self, field_callback = None):
        if not self.is_initialized:
            return
        
        for sp in SEASON_PARAMS:
            print("new season")
            self.field.set_flower_population(*sp)
            self.field.run_for(SEASON_LENGTH * CYCLE_LENGTH, field_callback)
    
    def get_critters(self):
        if self.social_critters:
            return self.field.agents_by_type[SocialCritter]
        else:
            return self.field.agents_by_type[Critter]
    
    def get_flowers(self):
        return self.field.agents_by_type[Flower]
    
    def get_nest(self) -> Nest:
        return self.field.agents_by_type[Nest][0]
    
    def save_dump(self, file_name):
        file = open(f"{RESULTS_FOLDER}/{file_name}.json", 'w')
        return json.dump(
            {
                "parameters": {
                    "field size": self.field.size(),
                    "critter count": len(self.get_critters()),
                    "social critters": self.social_critters
                },
                "nectar over time": self.get_nest().nectar_over_time,
                "nectar per cycle over time": self.get_nest().nectar_per_cycle
            },
            file
        )