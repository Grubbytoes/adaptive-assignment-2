import mesa
import random

from .field_agent import FieldAgent
from .flower import Flower

class Field(mesa.Model):
    def __init__(self, space_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.space = self.grid = mesa.space.ContinuousSpace(space_size, space_size, True)
        self.flower_population = 0
        self.target_flower_richness = 1
        self.target_flower_population = 0 # TODO
    
    # Runs the model for the given number of steps
    # optionally with a callback after each step, to which the self is passed as an argument 
    # (intended for visualization ie Pygame)
    def run_for(self, steps=1, field_callback=None):
        for i in range(steps):
            # Shuffle do agents
            self.agents.shuffle_do("step")
            if field_callback is not None:
                field_callback(self)
    
    # Plants a flower
    # if no position is given, a random one is picked
    # only flowers added by this method count towards the population
    def plant_flower(self, richness=5, pos=None):
        new_flower = Flower(self, richness)
        
        if pos == None:
            pos = self.random_position()
        
        self.place_agent(new_flower, *pos)
        self.flower_population += 1
    
    # Returns a random position on the field
    def random_position(self):
        pos = (
            random.randint(0, self.size()),
            random.randint(0, self.size()),
        )

        return pos

    # called each time a flower is killed
    # If this causes the known population to dip below the target, then a new one of equal richness is planted
    def on_flower_killed(self,):
        self.flower_population -= 1
        if self.flower_population < self.target_flower_population:
            self.plant_flower(richness=self.target_flower_richness)
    
    # Sets the target population of flowers as (no. flowers per 50 spaces squared)
    # as well as the richness of new flowers.
    # Then, so long as current population is below this target, new flowers are planted
    def set_flower_population(self, frequency=1, richness=5):
        self.target_flower_population = int(frequency * self.area() / (50**2))
        self.target_flower_richness = richness
        
        while self.flower_population < self.target_flower_population:
            self.plant_flower(self.target_flower_richness)

    # Returns height
    def size(self):
        return self.space.y_max
    
    def area(self):
        return self.size() ** 2
    
    # Places an agent on the field
    def place_agent(self, agent: FieldAgent, x, y):
        agent.place(self.space, x, y)