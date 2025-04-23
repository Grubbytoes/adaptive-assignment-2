from swarm_critters import *

# The job of this script is to take a newly instanced field and fill it with agents (nest, flowers, critters) in such a way
# that is conducive to the rest of our experiment

class EnvironmentManager:
    def __init__(self, field):
        self.field: Field = field
        self.is_initialized = False
    
    def initialize(self, critter_count = 8):
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
    
    def get_critters(self):
        return self.field.agents_by_type(Critter)
    
    def get_flowers(self):
        return self.field.agents_by_type(Flower)
    
    def get_nest(self):
        return self.field.agents_by_type(Nest)[0]