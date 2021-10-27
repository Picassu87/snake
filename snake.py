from turtle import Turtle
from scoreboard import Scoreboard

class Snake:
    def __init__(self, size, width, color, shape, starting_pos, starting_dir, max_speed, min_speed, name, number):
        self.speed_control_on = False
        self.dead = False
        self.triforce = 0
        self.number = number
        if name:
            self.name = name
        else:
            self.name = f"Player {number}"
        self.size = size
        self.width = width
        self.range = self.width/2
        self.range_timer = 0
        self.speed_timer = 0
        self.color = color
        self.shape = shape
        self.starting_pos = starting_pos
        self.starting_dir = starting_dir
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.speed = (max_speed+min_speed)//2
        self.body = []
        for i in range(self.size):
            t = Turtle(self.shape)
            t.color(self.color)
            t.shapesize(self.width / 20, self.width / 20)
            t.pu()
            t.speed("fastest")
            self.body.append(t)
            if self.starting_dir == "right":
                t.setpos(self.starting_pos[0] - self.width * i, self.starting_pos[1])
                self.body[0].seth(0)
            elif self.starting_dir == "left":
                t.setpos(self.starting_pos[0] + self.width * i, self.starting_pos[1])
                self.body[0].seth(180)
            elif self.starting_dir == "up":
                t.setpos(self.starting_pos[0], self.starting_pos[1] - self.width * i)
                self.body[0].seth(90)
            elif self.starting_dir == "down":
                t.setpos(self.starting_pos[0], self.starting_pos[1] + self.width * i)
                self.body[0].seth(270)
        # self.body[0].shape("triangle")
        # self.body[0].shapesize(1.1, 1.1)
        self.tail_pos = self.body[-1].pos()
        self.scoreboard = Scoreboard(color)
        self.has_turned = False

    def move(self):
        self.tail_pos = self.body[-1].pos()
        for i in range(len(self.body) - 1):
            self.body[-i - 1].setpos(self.body[-i - 2].pos())
        self.body[0].fd(self.width)

    def undo_move(self):
        for i in range(len(self.body) - 1):
            self.body[i].setpos(self.body[i+1].pos())
        self.body[-1].setpos(self.tail_pos)

    def grow(self):
        t = Turtle(self.shape)
        t.shapesize(self.width / 20, self.width / 20)
        t.color(self.color)
        t.pu()
        t.speed("fastest")
        t.setpos(self.tail_pos)
        self.body.append(t)

    def turn_right(self):
        if not self.has_turned:
            if self.body[0].heading() == 0:
                if self.speed > self.max_speed and self.speed_control_on:
                    self.speed -= 1
                    print(f"{self.name} speed up by one stage")
            elif self.body[0].heading() == 180:
                if self.speed < self.min_speed and self.speed_control_on:
                    self.speed += 1
                    print(f"{self.name} speed down by one stage")
            else:
                self.body[0].seth(0)
                self.has_turned = True

    def turn_up(self):
        if not self.has_turned:
            if self.body[0].heading() == 90:
                if self.speed > self.max_speed and self.speed_control_on:
                    self.speed -= 1
                    print(f"{self.name} speed up by one stage")
            elif self.body[0].heading() == 270:
                if self.speed < self.min_speed and self.speed_control_on:
                    self.speed += 1
                    print(f"{self.name} speed down by one stage")
            else:
                self.body[0].seth(90)
                self.has_turned = True

    def turn_left(self):
        if not self.has_turned:
            if self.body[0].heading() == 180:
                if self.speed > self.max_speed and self.speed_control_on:
                    self.speed -= 1
                    print(f"{self.name} speed up by one stage")
            elif self.body[0].heading() == 0:
                if self.speed < self.min_speed and self.speed_control_on:
                    self.speed += 1
                    print(f"{self.name} speed down by one stage")
            else:
                self.body[0].seth(180)
                self.has_turned = True

    def turn_down(self):
        if not self.has_turned:
            if self.body[0].heading() == 270:
                if self.speed > self.max_speed and self.speed_control_on:
                    self.speed -= 1
                    print(f"{self.name} speed up by one stage")
            elif self.body[0].heading() == 90:
                if self.speed < self.min_speed and self.speed_control_on:
                    self.speed += 1
                    print(f"{self.name} speed down by one stage")
            else:
                self.body[0].seth(270)
                self.has_turned = True
