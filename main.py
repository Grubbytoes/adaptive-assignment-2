import mesa

from swarm_critters import *

###

def main():
    field = Field(10, 10)
    
    nest = Nest(field)
        
    for i in range(5):
        new_critter = Critter(field, nest)
        field.place_agent(new_critter, i*2, 0)
    
    field.run_for(1)

###

main()
