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
        self.color_with_rocks = cfg['explorer_color_with_rocks']
        # MarsBaseEnum.A or MarsBaseEnum.B.
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
        # Next move to check.
        possible_x = self.x+self.dx
        possible_y = self.y+self.dy

        # Create a tuple of new points.
        offset = self.size/2
        possible_coord = ((possible_x-offset, possible_y+offset),
                          (possible_x+offset, possible_y-offset))

        # Can not move if outside of universe.
        if not is_in_world(possible_coord, self.universe):
            return False

        # Can not move if collides with other objects. (Except for other explorers)
        for other in self.universe.objects:
            # Allow collisions with other explorers.
            if isinstance(other, Explorer):
                continue
            if does_overlap(possible_coord, other):
                return False

        return True

    def tick(self):
        if self.carrying_rock:
            if self.base_in_reach():
                self.carrying_rock = False
                self.universe.n_rocks_collected += 1
            else:
                # Set dx and dy towards corresponding base.
                if self.team == MarsBaseEnum.A:
                    self.dx, self.dy = normalize(self.universe.command_center_a.x-self.x,
                                                 self.universe.command_center_a.y-self.y)
                if self.team == MarsBaseEnum.B:
                    self.dx, self.dy = normalize(self.universe.command_center_b.x-self.x,
                                                 self.universe.command_center_b.y-self.y)
        else:
            rocks = self.rocks_in_reach()
            # (TODO) Supports multiple collection of rocks.
            if len(rocks):
                # Pick up and remove rock.
                self.carrying_rock = True
                for rock in rocks:
                    self.universe.remove_object(rock)

        # Find a possible random move.
        while not self.can_move():
            self.dx, self.dy = self.compute_movement()

        self.move()
        self.ticks += 1

    def draw(self, canvas):
        force_field = Explorer(self.x, self.y, MarsBaseEnum.C, self.universe)
        force_field.size = 4 * self.sensor_range + self.size

        top_left, bottom_right = force_field.get_borders()
        canvas.create_oval(top_left[0],
                           top_left[1],
                           bottom_right[0],
                           bottom_right[1],
                           outline=self.sensor_color)

        top_left, bottom_right = self.get_borders()
        canvas.create_rectangle(top_left[0],
                                top_left[1],
                                bottom_right[0],
                                bottom_right[1],
                                fill=self.color_with_rocks if self.carrying_rock else self.color)

    def compute_movement(self):
        dx = random.uniform(-self.speed, self.speed)
        dy = random.uniform(-self.speed, self.speed)
        return normalize(dx, dy)