import mesa
import numpy as np

from collections import deque
from .field_agent import FieldAgent

class Nest(FieldAgent):
    colour = "firebrick1"
    type = "nest"
    
    def __init__(self, *args, cycle_length = 365, pheromone_queue_len=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.nectar = 0
        self.cycle_length = cycle_length
        self.pheromone_queue = deque()
        self.pheromone_queue_max_len = pheromone_queue_len
        
        # Performance monitoring
        self.nectar_last_cycle = 0
        self.nectar_over_time = []
        self.nectar_per_cycle = []
    
    def step(self):
        super().step()
    
        if self.step_count % self.cycle_length == self.cycle_length-1:
            self.log_cycle()           
    
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
    
    def log_cycle(self):
        nectar_this_cycle = self.nectar - self.nectar_last_cycle
        
        self.nectar_over_time.append(self.nectar)
        self.nectar_per_cycle.append(nectar_this_cycle)
        
        self.nectar_last_cycle = nectar_this_cycle
        