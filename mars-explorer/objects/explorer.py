# A Mars Explorer.
import copy
import random
import sys
sys.path.append("../../")

from queue import Queue
from objects.drawable_object import DrawableObject
from objects.obstacle import Obstacle
from utils.message_queue import MessageQueueA, MessageQueueB
from settings.base_config import cfg
from settings.constants import MarsBaseEnum
from settings.constants import UniverseEnum
from utils.calculation_utils import does_overlap, is_in_world, normalize

class Explorer(DrawableObject):
    def __init__(self, x, y, team, universe, multi_agent):
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
        # Multi-agent mode enabled.
        self.multi_agent = multi_agent
        # Multi-agent check to see if is listening to message.
        self.mission_rock = None
        # Multi-agent message queue to receive messages.
        self.message_queue = None
        if self.multi_agent:
            self.message_queue = MessageQueueA() if team == MarsBaseEnum.A else MessageQueueB()
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
        if self.universe.universe_type == UniverseEnum.MICROVERSE:
            # Check only using mars_base_a object.
            if does_overlap(self.get_borders(),
                            self.universe.command_center_a.get_borders(),
                            self.sensor_range):
                return True
        else:
            # Check if base in reach is the correct base.
            if self.team == MarsBaseEnum.A:
                if does_overlap(self.get_borders(),
                                self.universe.command_center_a.get_borders(),
                                self.sensor_range):
                    return True
            elif self.team == MarsBaseEnum.B:
                if does_overlap(self.get_borders(),
                                self.universe.command_center_b.get_borders(),
                                self.sensor_range):
                    return True
            else:
                print('ERROR::EXPLORER:: Unhandled team for explorer')
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
        possible_coord = ((possible_x-offset, possible_y-offset),
                          (possible_x+offset, possible_y+offset))

        # Can not move if outside of universe.
        if not is_in_world(possible_coord, self.universe):
            return False

        # Can not move if collides with other objects. (Except for other explorers)
        for other in self.universe.objects:
            # For now an obstacle is the only thing an explorer can not touch.
            if isinstance(other, Obstacle):
                if does_overlap(possible_coord, other):
                    return False

        return True

    # Multi-agent mode:
    #   When carrying a rock, it will concentrate on returning to base. However it will be able to get
    #   information for the other explorers in the team. If the explorer has a mission (rock message),
    #   it will resume to the messaged rock only after it offloads at base.
    #
    #   If not carrying a rock it will first try to get a message from the queue. If not, it will take
    #   a random move. If it reaches the message rock but if it is not there, it will either receive a
    #   new message or go to a random direction depending on the queue status.
    #
    #   An explorer will try to get a mission whenever possible.
    def tick(self):
        if self.multi_agent and self.mission_rock is None:
            # Try to get a new mission
            if not self.message_queue.empty():
                self.mission_rock = self.message_queue.get()
        # Check if it is multi_agent and if it is overlapping with the messaged rock.
        if self.multi_agent and self.mission_rock and does_overlap(self.get_borders(), self.mission_rock.get_borders()):
            self.mission_rock = None
        if self.carrying_rock:
            # Only checks for rocks while carrying a rock if in multi-agent mode to append to queue.
            if self.multi_agent:
                rocks = self.rocks_in_reach()
                for rock in rocks:
                    self.message_queue.put(copy.deepcopy(rock))
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
                # Pick up a single rock.
                self.universe.remove_object(rocks[0])
                # Dump the rest of the rocks into the queue if multiagent mode.
                if self.multi_agent:
                    for rock in rocks[1:]:
                        self.message_queue.put(copy.deepcopy(rock))
            else:
                # If multi-agent and did not find rock, go towards the mission rock.
                if self.multi_agent and self.mission_rock:
                    self.dx, self.dy = normalize(self.mission_rock.x-self.x,
                                                 self.mission_rock.y-self.y)

        # Find a possible random move.
        while not self.can_move():
            self.dx, self.dy = self.compute_movement()

        self.move()
        self.ticks += 1

    def draw(self, canvas):
        force_field = Explorer(self.x, self.y, MarsBaseEnum.C, self.universe, False)
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