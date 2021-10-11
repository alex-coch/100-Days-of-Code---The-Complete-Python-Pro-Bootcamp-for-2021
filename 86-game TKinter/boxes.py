import random

from turtle import Turtle





class Box(Turtle):



def __init__(self, pos):

super().__init__()

self.goto(pos)

self.colors = ['red', 'blue', 'green', 'yellow']

self.shape('square')

self.penup()

self.color(random.choice(self.colors))

self.shapesize(stretch_len=5, stretch_wid=2)