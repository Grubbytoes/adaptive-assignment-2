import mesa

from mymathstuff import vector2

class FieldAgent(mesa.Agent):
    colour = "darkslategray"
    type = "base"
    
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        
        self.step_count = 0
        
        self._space = None
        self._like_neighbors = (-1, [])
    
    def move(self, x, y):
        new_x = self.pos[0] + x
        new_y = self.pos[1] + y
        
        self._space.move_agent(self, (new_x, new_y))
        
    # Set the critters move_dir towards a position in space (normalizes by default)
    def move_towards(self, point, normalize=True):
        if normalize:
            self.move_dir = vector2.normalized(self.relative_position(point))
        else:
            self.move_dir = self.relative_position(point)
            
    def step(self):
        self.step_count += 1
    
    def relative_position(self, pos):
        return self._space.get_heading(self.pos, pos)
    
    def distance(self, pos):
        return self._space.get_distance(self.pos, pos)
            
    def field_neighbors(self, r):
        if not self.is_placed():
            return
        
        neighbors = [
            n 
            for n in self._space.get_neighbors(self.pos, r, False)
            if isinstance(n, FieldAgent)
        ]
        return neighbors
    
    def like_neighbors(self):
        if self._like_neighbors[0] == self.step_count:
            return self._like_neighbors[1]
        else:
            self._like_neighbors = (
                self.step_count,
                [n for n in self.vision if n.type == "critter"]
            )
            return self._like_neighbors[1]
    
    def is_placed(self):
        return self._space != None
    
    # If an other is provided, returns true of the relative position p of that other has a magnitude less than 1
    # if no other is provided, returns true if any other agents exist on the felid with in a 1 unit radius
    def is_touching(self, other=None):
        if other is None:
            return 0 < len(self.field_neighbors(1))
    
        return 1 > self._space.get_distance(self.pos, other.pos)
    
    def place(self, space, x=0, y=0):
        if self.is_placed():
            print(f"agent {self.unique_id} is already placed!")
            return
        
        self._space = space
        self._space.place_agent(self, (x, y))
    
    def kill(self):
        self.model.deregister_agent(self)
        self._space.remove_agent(self)