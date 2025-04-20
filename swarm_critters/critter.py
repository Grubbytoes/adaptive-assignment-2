import mesa
import numpy as np

from .field_agent import FieldAgent

class Critter(FieldAgent):

    def __init__(self, model, nest, sight_range=10):
        super().__init__(model)
        
        self.sight_range = max(sight_range, 1)
        self.velocity = np.zeros(2)
        self.nest = nest
        
    def step(self):
        super().step()
        print(f"{self.unique_id} - beep")

    def do_move(self):
        raise NotImplementedError("Critters cannot move yet!!")
    
    def see(self):
        if not self.is_placed():
            return
        
        vision = []
        field_of_vision = self.space.get_neighbors(self.pos, True, radius=self.sight_range)
        
        for other in field_of_vision:
            other_position = self.relative_position_of(other)
            distance = abs(other_position[0]) + abs(other_position[1])

            # vision entries are structured like so:
            #   [0] a reference to the object itself
            #   [1] the distance* to the object   * in von neumman/manhattan style
            
            item = (other, distance)
            vision.append(item)
        
        return vision
