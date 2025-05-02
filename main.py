import pygame
import threading

from environment_manager import EnvironmentManager
from swarm_critters import *

FIELD_SIZE = 320
SCALE = 2

# Pygame
pygame.init()
screen = pygame.display.set_mode((FIELD_SIZE * SCALE, FIELD_SIZE * SCALE))

# experiment params
CRITTER_COUNTS = {
    "small": 10,
    # "medium": 40,
    # "large": 160
}

def main():
    for key, item in CRITTER_COUNTS.items():
        env_lonely = EnvironmentManager(item, social_critters=False)
        env_social = EnvironmentManager(item, social_critters=True)
        
        thread_lonely = threading.Thread(target=run_and_record, args=[env_lonely, f"{key}.lonely"])
        thread_social = threading.Thread(target=run_and_record, args=[env_social,f"{key}.social"])
        
        thread_lonely.start()
        thread_social.start()
        
        thread_lonely.join()
        thread_social.join()

def run_and_record(environment: EnvironmentManager, file_name="untitled"):
    environment.run_environment()
    environment.save_dump(file_name)

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
