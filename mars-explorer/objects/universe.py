# This is where we save the game state.

import sys
sys.path.append("../../")

from .drawable_object import DrawableObject
from .explorer import Explorer
from .rock import Rock
from settings.base_config import cfg

class Universe(DrawableObject):

    def __init__(self, width, height, n_rocks, is_multiverse=False):
        self.width = width
        self.height = height

        self.objects = []
        self.rocks = []
        self.obstacles = []
        self.explorers = []
        self.n_rocks = n_rocks
        self.n_rocks_collected = 0
        # Is multiple mars bases. (For now only supports 2 bases)
        self.is_multiverse = is_multiverse

    def draw(self, canvas):
        canvas.configure(background=cfg['background_color'])

    def tick(self):
        for explorer in self.explorers:
            explorer.tick()

    def add_object(self, drawable_object):
        assert isinstance(drawable_object, DrawableObject)

        if isinstance(drawable_object, Explorer):
            self.explorers.append(drawable_object)
        elif isinstance(drawable_object, Rock):
            self.rocks.append(drawable_object)

        self.objects.append(drawable_object)

    def remove_object(self, drawable_object):
        assert isinstance(drawable_object, DrawableObject)

        if isinstance(drawable_object, Explorer):
            self.explorers.remove(drawable_object)
        elif isinstance(drawable_object, Rock):
            self.rocks.remove(drawable_object)

        self.objects.remove(drawable_object)

    def universe_is_no_more(self):
        return self.n_rocks == self.n_rocks_collected
