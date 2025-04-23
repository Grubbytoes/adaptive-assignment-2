import mesa

from .field_agent import FieldAgent

class Field(mesa.Model):
    def __init__(self, space_width, space_height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.space = self.grid = mesa.space.MultiGrid(space_width, space_height, True)
        self.width = space_width
        self.height = space_height
    
    def run_for(self, steps=1, field_callback=None):
        for i in range(steps):
            self.agents.shuffle_do("step")
            if field_callback is not None:
                field_callback(self)
            
    def place_agent(self, agent: FieldAgent, x, y):
        agent.place(self.space, x, y)