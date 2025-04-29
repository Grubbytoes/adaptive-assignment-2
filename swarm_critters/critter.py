import numpy as np

from dataclasses import dataclass
from mymathstuff import vector2
from .field_agent import FieldAgent

class Critter(FieldAgent):
    colour = "gold"
    type = "critter"
    confidence_multiplier = 1.2
    searching_turn_angle = 20

    SEARCHING = 's'
    HOMING = 'h'

    def __init__(self, model, nest, sight_range=5):
        super().__init__(model)

        self.sight_range = max(sight_range, 1)
        self.vision = []
        self.move_dir = vector2.rand()
        self.nest = nest
        self.state = Critter.SEARCHING

        # Hugo's algorithm
        self.confidence = 0
        self.clock = 0

    def step(self):
        super().step()

        # fill vision
        self.vision.clear()
        self.vision.extend(self.field_neighbors(self.sight_range))

        # state behaviour
        if self.state == Critter.HOMING:
            self.homing()
        elif self.state == Critter.SEARCHING:
            self.searching()
        else:
            # if we've somehow entered a bad state, return to the searching state
            self.state = Critter.SEARCHING

        # normalize, and turning noise, and move
        self.move_dir = random_turn(vector2.normalized(self.move_dir))
        self.move(*self.move_dir)

    # critter wanders along a straight line, searching for flowers
    def searching(self):
        other_flower = None # the closest flower
        other_critters = [] # all neighboring critters

        for other in self.vision:
            if other.type != "flower":
                continue

            if self.is_touching(other):
                other.take_nectar()
                self.clock = 0
                self.state = Critter.HOMING
                return
            else:
                self.move_towards(other.pos)

        # base
        if self.confidence <= 0:
            self.move_dir = random_turn(self.move_dir, Critter.searching_turn_angle)
        else:
            self.confidence = max(0, self.confidence - 1)

    # Critter will move towards the nest, and deposit nectar
    # then will pick a random direction and enter the wandering state
    def homing(self):
        if not self.is_touching(self.nest):
            self.move_towards(self.nest.pos)
            self.clock += 1
        else:
            self.state = Critter.SEARCHING
            self.nest.deposit_nectar()
            self.confidence = int(self.clock * Critter.confidence_multiplier)
            self.move_dir = np.multiply(self.move_dir, -1)

    def is_confident(self):
        return 0 < self.confidence

    # Incorporates separation steer of boid like behaviour into move_dir
    # defined as the sum of the negative relative distances to all nearby critters
    def separation(self, others, weight=1):
        if 1 > len(others):
            return

        steer = np.zeros(2)
        for other in others:
            steer = np.add(steer, np.negative(self.relative_position(other.pos)))

        if weight != 1:
            steer = np.multiply(steer, weight)

        self.move_dir = np.add(steer, self.move_dir)

    # Incorporates alignment
    # defined as the mean of the movement directions of all nearby critters
    def alignment(self, others, weight=1):
        if 1 > len(others):
            return

        directions = np.array([
            other.move_dir
            for other
            in others
        ])

        if 0 >= len(directions):
            return

        steer = np.mean(directions, 0)

        if weight != 1:
            steer = np.multiply(steer, weight)

        self.move_dir = np.add(steer, self.move_dir)

    # Incorporates cohesion
    # defined as the mean position of all nearby critters
    def cohesion(self, others, weight=1):
        if 1 > len(others):
            return

        positions = np.array([
            self.relative_position(other.pos)
            for other
            in others
        ])

        if 0 >= len(positions):
            return

        steer = np.mean(positions, 0)

        if weight != 1:
            steer = np.multiply(steer, weight)

        self.move_dir = np.add(steer, self.move_dir)


class SocialCritter(Critter):

    def __init__(self, model, nest, sight_range=5):
        super().__init__(model, nest, sight_range)

    def searching(self):
        super().searching()

        # If we've started homing, return early
        if self.state == Critter.HOMING:
            return

        # If we're confident then we don't care what anyone else is doing
        if self.is_confident():
            return

        to_avoid = []

        # Otherwise see what the others are doing
        for other in self.vision:
            if other.type != "critter":
                continue

            # if they're homing, go on the opposite direction to them
            if other.state == Critter.HOMING:
                self.confidence = other.clock
                self.move_dir = np.multiply(other.move_dir, -1)
                return
            # if they're confident, follow them
            elif other.is_confident():
                self.move_towards(other.pos)
                return
            # if they're searching avoid them
            else:
                to_avoid.append(other)

        # pass it on to boid logic
        self.separation(to_avoid)
    
    # Critter will move towards the nest, and deposit nectar
    # then will pick a random direction and enter the wandering state
    def homing(self):
        if not self.is_touching(self.nest):
            self.move_towards(self.nest.pos)
            self.clock += 1
        else:
            self.state = Critter.SEARCHING
            nest_instructions = self.nest.deposit_nectar(time=self.clock, direction=self.move_dir)

            # if no instructions, go back in the direction you came from
            # same if instructions would take longer than our clock (ie food is further away than the source we just visited)
            if nest_instructions == None or nest_instructions[0] > self.clock:
                self.confidence = int(self.clock * Critter.confidence_multiplier)
                self.move_dir = np.multiply(self.move_dir, -1)
            else:
                self.confidence = int(nest_instructions[0] * Critter.confidence_multiplier)
                self.move_dir = nest_instructions[1]  

def random_turn(v, amount=1):
    return vector2.rotated(v, np.random.randint(-amount, amount+1))