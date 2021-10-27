from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self, color):
        super().__init__()
        self.score = 0
        self.pencolor(color)
        self.alignment = "center"
        self.font = "Courier"
        self.font_size = 20
        self.pu()
        self.ht()

    def draw_arena(self, arena_size, grid_size):
        self.setpos(-arena_size[0]/2, -arena_size[1]/2)
        self.pd()
        self.pensize(grid_size-1)
        for _ in range(2):
            self.fd(arena_size[0])
            self.lt(90)
            self.fd(arena_size[1])
            self.lt(90)
        self.pu()
        self.setpos(-grid_size/4, arena_size[1]/2+grid_size/2)
        self.pensize(2*grid_size-2)
        self.pd()
        self.fd(grid_size/2)
        self.ht()

    def show_text(self, text, alignment, font, font_size, location):
        self.setpos(location)
        self.alignment = alignment
        self.font = font
        self.font_size = font_size
        self.write(text, False, self.alignment, (self.font, self.font_size, "normal"))

    def update(self, text):
        self.clear()
        self.write(text, False, self.alignment, (self.font, self.font_size, "normal"))
