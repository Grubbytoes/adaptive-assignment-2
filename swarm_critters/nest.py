import mesa
import numpy as np

from collections import deque
from .field_agent import FieldAgent

class Nest(FieldAgent):
    colour = "firebrick1"
    type = "nest"
    
    def __init__(self, *args, pheromone_queue_len=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.nectar = 0
        self.pheromone_queue = deque()
        self.pheromone_queue_max_len = pheromone_queue_len
    
    def step(self):
        super().step()       
    
    def deposit_nectar(self, time=0, direction=None):
        # Takes nectar deposited by a critter
        self.nectar += 1
        
        # Quid pro quo, if no useful information is deposited, none is given back
        if (time <= 0) or (direction is None):
            return None
        
        # enqueue
        self.pheromone_queue.append((time, np.multiply(direction, -1)))
        
        # dequeue (if full)
        if len(self.pheromone_queue) < self.pheromone_queue_max_len:
            return None # ie a signal to just go back in their direction
        else:
            return self.pheromone_queue.popleft()        