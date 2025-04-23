import mesa

from .field_agent import FieldAgent

class Nest(FieldAgent):
    colour = "firebrick1"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs), 