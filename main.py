import pygame

from swarm_critters import *

FIELD_SIZE = 64
SCALE = 4

# Pygame
pygame.init()
screen = pygame.display.set_mode((FIELD_SIZE * SCALE, FIELD_SIZE * SCALE))

###

def main():
    field = Field(FIELD_SIZE, FIELD_SIZE)
    
    # make nest
    nest = Nest(field)
    field.place_agent(nest, 16, 14)
    
    # make critters 
    for i in range(5):
        new_critter = Critter(field, nest)
        field.place_agent(new_critter, 10 + i*2, 16)
    
    for i in range(100):    
        field.run_for(1)
        draw_field(field)


def draw_field(field: Field, delay=40):  
    # refresh the screen
    screen.fill("aliceblue")
    
    # draw agents
    for agent in field.agents:
        # check agent exists in space
        if agent.pos is None:
            continue
        
        agent_representation = pygame.Rect(
            agent.pos[0] * SCALE,
            agent.pos[1] * SCALE,
            SCALE,
            SCALE
        )
        pygame.draw.rect(screen, agent.colour, agent_representation)
    
    pygame.time.delay(delay)
    pygame.display.flip()       


###

main()
