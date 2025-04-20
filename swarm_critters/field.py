import mesa

from .field_agent import FieldAgent

class Field(mesa.Model):
    def __init__(self, space_width, space_height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.space = self.grid = mesa.space.SingleGrid(space_width, space_height, True)
    
    def run_for(self, steps=1):
        for i in range(steps):
            self.agents.shuffle_do("step")
            
    def place_agent(self, agent: FieldAgent, x, y):
        agent.place(self.space, x, y)