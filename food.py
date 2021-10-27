import turtle

class Food(turtle.Turtle):
    def __init__(self, size, shape, color, effect, value, timer):
        super().__init__()
        self.size = size
        self.shape(shape)
        self.has_random_color = False
        if color == "random":
            self.color("white")
            self.has_random_color = True
        else:
            self.color(color)
        self.effect = effect
        self.value = value
        self.timer = timer
        self.seth(90)
        self.ht()
        self.pu()
        self.speed("fastest")
        self.shapesize(self.size/20, self.size/20)
