from tkinter import Tk, Canvas

class GUI(object):
    def __init__(self, universe):
        self.ticks = 0
        self.universe = universe
        self.width = universe.width
        self.height = universe.height

        self.window = Tk()
        self.window.title("Mars Explorer")

        temp_x, temp_y = self.get_window_coordinates()
        self.window.geometry(
              '%dx%d+%d+%d' % (
                    self.width, self.height, temp_x, temp_y))

        self.canvas = Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.after(1, self.tick())

    def start(self):
        print('GUI:: Starting loop...')
        self.window.mainloop()

    def get_window_coordinates(self):
        # Get screen width and height.
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        # Get x and y
        window_x = screen_width/2 - self.width/2
        window_y = screen_height/2 - self.height/2
        return window_x, window_y

    def tick(self):
        # Stop if done.
        if self.universe.universe_is_no_more():
            return

        self.universe.tick()
        self.draw()

        self.ticks += 1
        self.canvas.after(1, self.tick)

    def draw(self):
        self.canvas.delete('all')
        self.universe.draw(self.canvas)
        for obj in self.universe.objects:
              obj.draw(self.canvas)

        self.canvas.create_text(70, 10, text=str(self.ticks))
        self.canvas.create_text(70, 50, text='Rocks delivered: %d' % self.universe.n_rocks_collected)
        self.canvas.create_text(70, 70, text='Total rocks: %d' % self.universe.n_rocks)

