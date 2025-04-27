import pygame

from environment_manager import EnvironmentManager
from swarm_critters import *

FIELD_SIZE = 160
SCALE = 4

# Pygame
pygame.init()
screen = pygame.display.set_mode((FIELD_SIZE * SCALE, FIELD_SIZE * SCALE))

###

def main():
    _field = Field(FIELD_SIZE, FIELD_SIZE)
    environment_manager = EnvironmentManager(_field)
    
    environment_manager.initialize(20, .02)
    environment_manager.field.run_for(500, draw_field) # oh my god this is evil


def draw_field(field: Field, delay=40):  
    # refresh the screen
    screen.fill("aliceblue")
    
    # draw agents
    for agent in field.agents:
        # check agent exists in space
        if agent.pos is None:
            continue
        
        agent_coords = (
            agent.pos[0] * SCALE,
            agent.pos[1] * SCALE,
        )
        pygame.draw.circle(screen, agent.colour, agent_coords, SCALE/2)
    
    pygame.time.delay(delay)
    pygame.display.flip()       


###

main()
