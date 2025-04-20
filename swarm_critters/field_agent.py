import mesa

class FieldAgent(mesa.Agent):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        
        self.step_count = 0
        
        self._space = None
    
    def step(self):
        self.step_count += 1
        
    def relative_position_of(self, other: mesa.Agent):
        x_relative = int(other.pos[0] - self.pos[0])
        y_relative = int(other.pos[1] - self.pos[1])
        
        return (x_relative, y_relative)
    
    def is_placed(self):
        return self._space != None
    
    def place(self, space, x=0, y=0):
        if self.is_placed():
            print(f"agent {self.unique_id} is already placed!")
            return
        
        self._space = space
        self._space.place_agent(self, (x, y))