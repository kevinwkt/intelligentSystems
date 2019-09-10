# A Mars Explorer.
import random
import sys
sys.path.append("../../")

from objects.drawable_object import DrawableObject
from settings.base_config import cfg
from settings.constants import MarsBaseEnum
from settings.constants import UniverseEnum
from utils.calculation_utils import does_overlap, is_in_world, normalize

class Explorer(DrawableObject):
    def __init__(self, x, y, team, universe):
        # Current centroid x and y coord.
        self.x = x
        self.y = y
        # Size of explorer.
        self.size = cfg['explorer_size']
        # Color of explorer object.
        self.color = cfg['explorer_color']
        # UniverseEnum.MICROVERSE or UniverseEnum.MULTIVERSE.
        self.team = team
        # Speed of the explorer.
        self.speed = cfg['explorer_speed']
        # Copy of universe.
        self.universe = universe
        # Vector to apply.
        self.dx, self.dy = self.compute_movement()
        # Sensor range to pick up objects.
        self.sensor_range = cfg['sensor_range']
        # Poll time to use sensor.
        self.sensor_delay = cfg['sensor_delay']
        # Color of the sensor force field.
        self.sensor_color = cfg['sensor_color']
        # State of explorer.
        self.carrying_rock = False
        # Counter for poll time for sensor.
        self.ticks = 0
        # (TODO) How many rocks it is carrying.
        self.n_rocks = 0

    def rocks_in_reach(self):
        # Wait for sensor poll time since it is expensive.
        if self.ticks < self.sensor_delay:
            return []

        rocks = []
        for rock in self.universe.rocks:
            if does_overlap(self, rock, self.sensor_range):
                rocks.append(rock)
        # Reset sensor poll time.
        self.ticks = 0
        return rocks

    def base_in_reach(self):
        # if self.universe.universe_type == UniverseEnum.MICROVERSE:
        #     # Check only using mars_base_a object.
        #     if does_overlap(self.get_borders(),
        #                     self.universe.mars_base.get_borders(),
        #                     self.sensor_range):
        #         return True
        # else:
        #     # Check if base in reach is the correct base.
        #     if does_overlap(self.get_borders(),
        #                     self.universe.mars_base.get_borders(),
        #                     self.sensor_range):
        #         return True
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

    def draw(self, canvas):
        force_field = Explorer(self.x, self.y, self.world)
        force_field.size = 2 * self.sensor_range + self.size

        top_left, bottom_right = force_field.get_borders()
        canvas.create_oval(top_left.x,
                           top_left.y,
                           bottom_right.x,
                           bottom_right.y,
                           outline=self.sensor_color)

        top_left, bottom_right = self.get_borders()
        canvas.create_rectangle(top_left.x,
                                top_left.y,
                                bottom_right.x,
                                bottom_right.y,
                                fill=self.HAS_ROCK_COLOR if self.has_rock else self.COLOR)

    def compute_movement(self):
        dx = random.uniform(-self.speed, self.speed)
        dy = random.uniform(-self.speed, self.speed)
        return normalize(dx, dy)