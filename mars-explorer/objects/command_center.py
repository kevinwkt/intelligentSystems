# An mars rover controller... In mars...

import pathlib
import sys
sys.path.append("../../")

from PIL import Image, ImageTk
from .drawable_object import DrawableObject
from settings.base_config import cfg

class CommandCenter(DrawableObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = cfg['command_center_size']
        # self.image = Image.open(pathlib.Path("./assets/command_center.jpg")).resize((self.size, self.size))
        self.image = Image.open(pathlib.Path("./assets/base.jpeg")).resize((self.size, self.size))

    def draw(self, canvas):
        self.tkimg = ImageTk.PhotoImage(image=self.image)
        canvas.create_image(self.x,
                            self.y,
                            image=self.tkimg)
