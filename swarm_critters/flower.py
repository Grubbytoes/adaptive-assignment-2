from .field_agent import FieldAgent

class Flower(FieldAgent):
    colour = "darkorchid2"
    type = "flower"
    
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        
        self.pollen = 5
    
    # has pollen taken by a critter
    def take_pollen(self):
        self.pollen -= 1
        if 0 >= self.pollen:
            self.kill()
        