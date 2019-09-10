# A rock object... In mars...
import pathlib
import random
import sys
sys.path.append("../../")

from .drawable_object import DrawableObject
from settings.base_config import cfg
from utils.calculation_utils import does_overlap, is_in_world

class Rock(DrawableObject):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = cfg['rock_size']
        self.color = cfg['rock_color']

    def draw(self, canvas):
        canvas.create_oval(self.get_borders()[0][0],
                           self.get_borders()[0][1],
                           self.get_borders()[1][0],
                           self.get_borders()[1][1],
                           fill=self.color)

    def can_exist(self,universe):
        if not is_in_world(self, universe):
            return False
        for obj in universe.objects:
            if does_overlap(obj, self):
                return False
        return True

    def create_rocks(n_rocks, universe):
        rocks = []
        while n_rocks > len(rocks):
            x = random.randint(0, universe.width)
            y = random.randint(0, universe.height)
            rock = Rock(x, y)
            if rock.can_exist(universe):
                rocks.append(rock)

        return rocks

