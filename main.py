import pygame

from environment_manager import EnvironmentManager
from swarm_critters import *

FIELD_SIZE = 180
SCALE = 4

# Pygame
pygame.init()
screen = pygame.display.set_mode((FIELD_SIZE * SCALE, FIELD_SIZE * SCALE))

###

def main():
    environment_manager = EnvironmentManager(FIELD_SIZE, 20, True)
    environment_manager.run_environment()
    print(environment_manager.save_dump("social results"))


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
