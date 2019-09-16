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
        obj1_top_left, obj1_bottom_right = object1.get_borders()
    else:
        # Else assume object1 is a tuple of points.
        obj1_top_left, obj1_bottom_right = object1

    if isinstance(object2, DrawableObject):
        # If object1 is an object depack.
        obj2_top_left, obj2_bottom_right = object2.get_borders()
    else:
        # Else assume object1 is a tuple of points.
        obj2_top_left, obj2_bottom_right = object2

    return (
        # Check for x axis first.
        obj1_top_left[0] - epsilon < obj2_bottom_right[0] and
        obj1_bottom_right[0] + epsilon > obj2_top_left[0] and
        # Check for y axis second.
        obj1_top_left[1] - epsilon < obj2_bottom_right[1] and
        obj1_bottom_right[1] + epsilon > obj2_top_left[1])

def compute_ab(a, b):
    return math.sqrt(a**2 + b**2)

def normalize(a, b):
    ab = compute_ab(a, b)
    return a / ab, b / ab