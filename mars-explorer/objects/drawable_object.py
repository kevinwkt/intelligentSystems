# Abstract drawable object to implement.

class DrawableObject(object):
    def draw(self, canvas):
        raise NotImplementedError()

    # Returns bottom left corner and top right corner.
    # ((x1, y1), (x2, y2)).
    def get_borders(self):
        offset = self.size/2
        return ((self.x-offset, self.y-offset), (self.x+offset, self.y+offset))
