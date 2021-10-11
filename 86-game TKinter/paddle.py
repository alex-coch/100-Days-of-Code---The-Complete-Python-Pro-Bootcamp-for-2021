from turtle import Turtle





class Paddle(Turtle):
    def __init__(self, pos):
        super().__init__()
        self.create_paddle(pos)



    def create_paddle(self, pos):
        self.shape('square')
        self.color('white')
        self.penup()
        self.goto(pos)
        self.shapesize(stretch_len=10, stretch_wid=1)



    def move_right(self):
        if self.xcor() < 490:
            x = self.xcor() + 20
            y = self.ycor()
            self.goto(x, y)



    def move_left(self):
        if self.xcor() > -490:
            x = self.xcor() - 20
            y = self.ycor()
            self.goto(x, y)