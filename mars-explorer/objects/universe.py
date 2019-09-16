# This is where we save the game state.

import sys
sys.path.append("../../")

from .drawable_object import DrawableObject
from .command_center import CommandCenter
from .explorer import Explorer
from .obstacle import Obstacle
from .rock import Rock
from settings.base_config import cfg
from settings.constants import MarsBaseEnum

class Universe(DrawableObject):

    def __init__(self, width, height, n_rocks, universe_type):
        # Dimensions of the universe.
        self.width = width
        self.height = height

        # Mars bases. (Currently supports maximum of 2)
        self.command_center_a = None
        self.command_center_b = None

        # List of all the objects in the universe.
        self.objects = []
        # List of rocks.
        self.rocks = []
        # List of obstacles.
        self.obstacles = []
        # List of explorers.
        self.explorers = []
        # Total number of rocks to be collected.
        self.n_rocks = n_rocks
        # Current number of rocks to be collected
        self.n_rocks_collected = 0
        # Is multiple mars bases. (For now only supports 2 bases)
        self.universe_type = universe_type

    def draw(self, canvas):
        canvas.configure(background=cfg['background_color'])

    def tick(self):
        for explorer in self.explorers:
            explorer.tick()

    def add_object(self, drawable_object, enum_check=None):
        assert isinstance(drawable_object, DrawableObject)

        if isinstance(drawable_object, Explorer):
            self.explorers.append(drawable_object)
        elif isinstance(drawable_object, Rock):
            self.rocks.append(drawable_object)
        elif isinstance(drawable_object, Obstacle):
            self.obstacles.append(drawable_object)
        elif isinstance(drawable_object, CommandCenter) and enum_check==MarsBaseEnum.A:
            print('creating command_center_a')
            self.command_center_a = drawable_object
        elif isinstance(drawable_object, CommandCenter) and enum_check==MarsBaseEnum.B:
            self.command_center_b = drawable_object
        else:
            print('ERROR::UNIVERSE:: Unhandled add_object')

        self.objects.append(drawable_object)

    def remove_object(self, drawable_object, enum_check=None):
        assert isinstance(drawable_object, DrawableObject)

        if isinstance(drawable_object, Explorer):
            self.explorers.remove(drawable_object)
        elif isinstance(drawable_object, Rock):
            self.rocks.remove(drawable_object)
        elif isinstance(drawable_object, Obstacle):
            self.obstacles.remove(drawable_object)
        elif isinstance(drawable_object, CommandCenter) and enum_check==MarsBaseEnum.A:
            self.command_center_a = None
        elif isinstance(drawable_object, CommandCenter) and enum_check==MarsBaseEnum.B:
            self.command_center_b = None

        self.objects.remove(drawable_object)

    def universe_is_no_more(self):
        return self.n_rocks == self.n_rocks_collected
