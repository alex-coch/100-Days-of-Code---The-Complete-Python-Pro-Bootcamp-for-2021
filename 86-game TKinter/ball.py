from turtle import Turtle





class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color('red')
        self.shape('circle')
        self.penup()
        self.goto(0, -170)
        self.x = 10
        self.y = 10

def refresh(self):
    x = self.xcor() + self.x
    y = self.ycor() + self.y
    self.goto(x, y)

def bouncex(self):
    self.x *= -1

def bouncey(self):
    self.y *= -1

def restart(self):
    self.goto(0, 0)
    self.bouncey()
    self.bouncex()