from .field_agent import FieldAgent

class Flower(FieldAgent):
    colour = "darkorchid2"
    
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        
        self.pollen = 5