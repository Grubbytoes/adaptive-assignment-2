import random
import json

from numpy import mean

from swarm_critters import *
from math import pow, sqrt

RESULTS_FOLDER = "results"
CYCLE_LENGTH = 500
SEASON_LENGTH = 12
SEASON_PARAMS = (
    (2, 10), # SPRING
    (4, 10), # SUMMER
    (4, 5), # AUTUMN
    (.5, 50) # WINTER
)

def field_size(c):
    size = int(sqrt(c) * 50.63)
    return size

# This script runs the experiment with a single set of parameters

class EnvironmentManager:
    def __init__(self, critter_count=8, social_critters=False):
        self.field: Field = Field(field_size(critter_count))
        self.nest = None
        self.is_initialized = False
        self.social_critters = social_critters
        
        self.flower_population_sizes = []
        self.average_flower_richness = []
        self.nectar_gathered = []
        self.nectar_pcycle_pcritter = []
        
        self.data_register = {}
        
        self._initialize(critter_count, social_critters)
    
    def run_environment(self, field_callback = None):
        if not self.is_initialized:
            return
        
        for sp in SEASON_PARAMS:
            print("new season")
            self.field.set_flower_population(*sp)
            for i in range(SEASON_LENGTH):
                self.run_cycle()
    
    def run_cycle(self):
        # run cycle
        self.field.run_for(CYCLE_LENGTH)
        
        # record data       
        nectar_this_cycle = self.nest.nectar
        if len(self.nectar_gathered) > 0:
            nectar_this_cycle -= self.nectar_gathered[-1]
        flowers = self.get_flowers()
        
        self.nectar_gathered.append(self.nest.nectar)
        self.nectar_pcycle_pcritter.append(
            nectar_this_cycle / self.get_critter_count()
        )
        self.flower_population_sizes.append(len(flowers))
        self.average_flower_richness.append(mean([f.richness for f in flowers]))
            
    
    def get_critters(self):
        if self.social_critters:
            return self.field.agents_by_type[SocialCritter]
        else:
            return self.field.agents_by_type[Critter]
    
    def get_flowers(self):
        return self.field.agents_by_type[Flower]
    
    def get_nest(self) -> Nest:
        return self.nest
    
    def get_critter_count(self):
        return len(self.get_critters())
    
    def save_dump(self, file_name):
        file = open(f"{RESULTS_FOLDER}/{file_name}.json", 'w')
        return json.dump(
            {
                "field size": self.field.size(),
                "critter count": self.get_critter_count(),
                "social critters": self.social_critters,
                "flower population": self.flower_population_sizes,
                "mean flower richness": self.average_flower_richness,
                "nectar gathered": self.nectar_gathered,
                "nectar/cycle/critter": self.nectar_pcycle_pcritter,
            },
            file
        )
       
    def _initialize(self, critter_count=8, social_critters=True):
       
        if self.is_initialized:
            print(f"WARNING: {self} is already initialized")
            return
        
        # 1. place the nest in the center
        nest = Nest(self.field, pheromone_queue_len=12)
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
        self.nest = nest
        