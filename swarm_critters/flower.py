from .field_agent import FieldAgent

class Flower(FieldAgent):
    colour = "darkorchid2"
    type = "flower"
    
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        
        self.nectar = 5
    
    # has pollen taken by a critter
    def take_nectar(self):
        self.nectar -= 1
        if 0 >= self.nectar:
            self.kill()
        