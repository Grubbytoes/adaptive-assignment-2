from .field_agent import FieldAgent

class Flower(FieldAgent):
    colour = "darkorchid2"
    type = "flower"
    
    def __init__(self, model, richness, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        
        self.richness = richness
        self.nectar = richness
    
    # has pollen taken by a critter
    def take_nectar(self):
        self.nectar -= 1
        if 0 >= self.nectar:
            self.kill()
    
    def kill(self):
        # TODO
        self.model.on_flower_killed()
        return super().kill()
        