from turtle import Turtle





class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.points = 0
        self.missed = 0

    def update(self):
        self.clear()
        self.points += 1
        self.goto(570, 330)
        self.write(f"Score: {self.points}", align='right', font=('Courier', 20, 'normal'))


    def reset(self):
        self.clear()
        self.points = 0
        self.goto(570, 330)
        self.write(f"Score: {self.points}", align='right', font=('Courier', 20, 'normal'))