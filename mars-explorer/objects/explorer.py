# A Mars Explorer.
import random
import sys
sys.path.append("../../")

from .drawable_object import DrawableObject
from settings.base_config import cfg
from utils.calculation_utils import does_overlap, is_in_world, normalize

class Explorer(DrawableObject):
    def __init__(self, x, y, universe):
        self.x = x
        self.y = y
        self.speed = cfg['explorer_speed']
        self.universe = universe
        self.dx, self.dy = self.compute_movement()
        self.sensor_range = cfg['sensor_range']
        self.sensor_delay = cfg['sensor_delay']
        self.carrying_rock = False
        self.n_rocks = 0
        self.ticks = 0
        self.size = cfg['explorer_size']
        self.color = cfg['explorer_color']

    def rocks_in_reach(self):
        # Wait for sensor since it is expensive.
        if self.ticks < self.sensor_delay:
            return []

        rocks = []
        for rock in self.universe.rocks:
            if does_overlap(self, rock, self.sensor_range):
                rocks.append(rock)
        self.ticks = 0
        return rocks

    def base_in_reach(self):
        if does_overlap(self.get_corners(),
                        self.universe.mars_base.get_bounds(),
                        self.PICKUP_REACH):
            return True
        return False

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def can_move(self):
        pass

    def tick(self):
        if carrying_rock:
            if self.base_in_reach():
                self.carrying_rock = False
                self.universe.n_rocks_collected += 1
            else:
                # Set dx and dy towards base.
                pass
        else:
            # Check if near rock
            rocks = self.rocks_in_reach()
            if len(rocks):
                # Pick up and remove rock.
                self.carrying_rock = True
                self.universe.remove_object(rocks[0])

        # Find a possible random move.
        while not self.can_move():
            self.dx, self.dy = self.compute_movement()

        self.move()
        self.ticks += 1

    def draw():
        pass

    def compute_movement(self):
        dx = random.uniform(-self.speed, self.speed)
        dy = random.uniform(-self.speed, self.speed)
        return normalize(dx, dy)