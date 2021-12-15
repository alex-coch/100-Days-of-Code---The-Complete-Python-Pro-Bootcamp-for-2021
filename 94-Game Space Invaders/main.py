from turtle import Screen, Turtle
import time
from random import choice

screen = Screen()
screen.bgcolor("black")
screen.setup(800, 600)
screen.title("Space Invaders")
screen.tracer(0)
screen.colormode(255)


# ------------------------INITIALIZE THE SHIP-------------------#
class Ship(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("arrow")
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.color("white")
        self.up()
        self.setheading(90)
        self.goto(0, -270)

    def go_right(self):
        new_x = self.xcor() + 15
        self.goto(new_x, self.ycor())

    def go_left(self):
        new_x = self.xcor() - 15
        self.goto(new_x, self.ycor())

    def shoot(self):
        shot = Shot()
        shot.goto(self.xcor(), self.ycor() + 15)


ship = Ship()
screen.listen()
screen.onkeypress(ship.go_left, "Left")
screen.onkeypress(ship.go_right, "Right")
screen.onkeypress(ship.shoot, "space")


# ------------------------SHOOTING-------------------#

class Shot(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(stretch_wid=0.4, stretch_len=0.6)
        self.color("white")
        self.up()
        self.setheading(90)
        shots_fired.append(self)


shots_fired = []

# ------------------------INITIALIZE THE ENEMIES-------------------#
colorlist = [(249, 212, 93), (150, 69, 97), (53, 99, 155), (232, 137, 62), (107, 174, 211), (243, 237, 241),
             (114, 83, 59), (201, 146, 177), (200, 77, 109), (145, 134, 72), (230, 90, 59), (141, 192, 140),
             (72, 103, 90), (68, 162, 92), (5, 165, 179), (227, 161, 183), (115, 126, 142), (163, 196, 221),
             (16, 66, 123), (187, 24, 34), (13, 56, 103), (235, 172, 160), (175, 201, 179), (163, 200, 215),
             (186, 27, 25), (80, 55, 37), (96, 61, 30)]

enemy_placement = [(-360, 270), (-280, 270), (-200, 270), (-120, 270), (-40, 270), (40, 270), (120, 270), (200, 270),
                   (280, 270), (360, 270), (-360, 230), (-280, 230), (-200, 230), (-120, 230), (-40, 230), (40, 230),
                   (120, 230), (200, 230), (280, 230), (360, 230)]


class Enemy(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.color(choice(colorlist))
        self.up()
        self.goto(position)


enemy_list = []

enemy_list.append(Enemy(choice(enemy_placement)))


# ------------------------PLAYING THE GAME-------------------#


def move_stuff():
    global game_on
    for shot in shots_fired:
        new_shot_y = shot.ycor() + 5
        shot.goto(shot.xcor(), new_shot_y)
        if shot.ycor() > 300:
            shots_fired.remove(shot)
            del shot

    for enemy in enemy_list:
        new_enemy_y = enemy.ycor() - 1
        enemy.goto(enemy.xcor(), new_enemy_y)
        if enemy.ycor() < -235:
            game_on = False

    for shot in shots_fired:
        for enemy in enemy_list:
            if shot.distance(enemy) < 30:
                enemy.goto(500, 500)
                shot.goto(500, 500)
                enemy_list.remove(enemy)
                shots_fired.remove(shot)
                enemy_list.append(Enemy(choice(enemy_placement)))
                enemy_list.append(Enemy(choice(enemy_placement)))


game_on = True

while game_on:
    time.sleep(0.02)
    screen.update()
    move_stuff()

screen.exitonclick()