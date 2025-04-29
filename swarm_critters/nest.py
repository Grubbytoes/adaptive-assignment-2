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
        self.nectar_per_cycle = []
        self.pheromone_queue = deque()
        self.pheromone_queue_max_len = pheromone_queue_len
    
    def step(self):
        super().step()
    
        if self.step_count % self.cycle_length == self.cycle_length-1:
            self.nectar_per_cycle.append(self.nectar)
            print(self.nectar_per_cycle)
            
    
    def deposit_nectar(self, time=0, direction=None):
        # Takes nectar deposited by a critter
        self.nectar += 1
        
        # enqueue
        self.pheromone_queue.append((time, np.multiply(direction, -1)))
        
        # dequeue (if full)
        if len(self.pheromone_queue) < self.pheromone_queue_max_len:
            return None # ie a signal to just go back in their direction
        else:
            return self.pheromone_queue.popleft()
        