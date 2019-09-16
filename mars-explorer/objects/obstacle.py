# An obstacle... In mars...

import random
import sys
sys.path.append("../../")

from .drawable_object import DrawableObject
from settings.base_config import cfg
from utils.calculation_utils import does_overlap, is_in_world

class Obstacle(DrawableObject):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = cfg['obstacle_size']
        self.color = cfg['obstacle_color']

    def draw(self, canvas):
        canvas.create_rectangle(self.get_borders()[0][0],
                                self.get_borders()[0][1],
                                self.get_borders()[1][0],
                                self.get_borders()[1][1],
                                fill=self.color)

    def can_exist(self, universe):
        if not is_in_world(self, universe):
            return False
        for obj in universe.objects:
            if does_overlap(obj, self):
                return False
        return True

    def create_obstacles(n_obstacles, universe):
        # Auxiliary function to not have obstacles blocking indefinitely explorers.
        def overlaps_with_current(obj1, current_obstacles):
            for current in current_obstacles:
                if does_overlap(obj1, current, obj1.size):
                    return True
            return False

        obstacles = []
        while len(obstacles) < n_obstacles:
            x = random.randint(0, universe.width)
            y = random.randint(0, universe.height)
            obstacle = Obstacle(x, y)
            if obstacle.can_exist(universe) and not overlaps_with_current(obstacle, obstacles):
                obstacles.append(obstacle)

        return obstacles
