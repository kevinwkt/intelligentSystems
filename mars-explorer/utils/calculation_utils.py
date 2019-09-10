# Utility lib for calculation.
import math
import sys
sys.path.append("../")

from objects.drawable_object import DrawableObject

def is_in_world(object1, universe):
    if isinstance(object1, DrawableObject):
        # If object1 is an object depack.
        if (object1.get_borders()[0][0] < 0 or object1.get_borders()[0][1] < 0 or
            object1.get_borders()[1][0] > universe.width or object1.get_borders()[1][1] > universe.height):
            return False
    else:
        # Else assume object1 is a tuple of points.
        if (object1[0][0] < 0 or object1[0][1] < 0 or
            object1[1][0] > universe.width or object1[1][1] > universe.height):
            return False
    return True

def does_overlap(object1, object2, epsilon=0):
    if isinstance(object1, DrawableObject):
        # If object1 is an object depack.
        return (object1.get_borders()[0][0] - epsilon < object2.get_borders()[1][0] and
                object1.get_borders()[1][0] + epsilon > object2.get_borders()[0][0] and
                object1.get_borders()[0][1] - epsilon < object2.get_borders()[1][1] and
                object1.get_borders()[1][1] + epsilon > object2.get_borders()[0][1])
    else:
        # Else assume object1 is a tuple of points.
        return (object1[0][0] - epsilon < object2.get_borders()[1][0] and
                object1[1][0] + epsilon > object2.get_borders()[0][0] and
                object1[0][1] - epsilon < object2.get_borders()[1][1] and
                object1[1][1] + epsilon > object2.get_borders()[0][1])

def compute_ab(a, b):
    return math.sqrt(a**2 + b**2)

def normalize(a, b):
    ab = compute_ab(a, b)
    return a / ab, b / ab