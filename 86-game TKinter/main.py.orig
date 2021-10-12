import time
from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from score import Score
from boxes import Box


# Creates the main game screen
screen = Screen()
screen.setup(1200, 720)
screen.bgcolor('black')
screen.title('Breakout Game')
screen.tracer(0)

paddle = Paddle((0, -345)) # creates the paddle used to hit the ball
ball = Ball() # creates the ball
score = Score() # displays the score in the top right corner
final_msg = Score() # displays the final msg after game is finished

# generates and displays boxes with random colors and sizes
x = -545
y = 300
boxes = []
for i in range(77):
    box = Box((x, y))
    boxes.append(box)
    if x < 510:
        x = box.xcor() + 108
    else:
        x = -545
        y = box.ycor() - 50

screen.listen() # enabling listeners
screen.onkeypress(paddle.move_left, 'Left') # moves paddle left when left-arrow is pressed
screen.onkeypress(paddle.move_right, 'Right') # moves paddle right when right-arrow is pressed

# while loop runs till all boxes are not hit by ball
game_is_on = True
while game_is_on:
    screen.update()
    ball.refresh()
    time.sleep(0.03)

    # bounces after touching right or left side
    if ball.xcor() > 570 or ball.xcor() < -570:
        ball.bouncex()

    # bounces after touching upper side
    if ball.ycor() > 340:
        ball.bouncey()

    # checks if ball hits the paddle then bounces the ball back
    if paddle.xcor() - 105 < ball.xcor() < paddle.xcor() + 105 and ball.ycor() < paddle.ycor() + 17 and ball.ycor() < -320:
        ball.bouncey()

    # restarts when paddle misses to hit the ball
    if ball.ycor() < -350:
        ball.restart()
        score.missed += 1
        print(f'You missed the ball {score.missed} time/times.')

    # check if the ball hits the box
    for b in boxes:
        if b.xcor() - 50 < ball.xcor() < b.xcor() + 50 and b.ycor() - 30 < ball.ycor() < b.ycor() + 30:
            b.goto(1000, 0)
            ball.bouncey()
            score.update()
            boxes.remove(b)

    if len(boxes) == 0:
        ball.goto(1000, 0)
        screen.update()
        game_is_on = False

final_msg.goto(0, 0)
win_msg = 'Yeah you won!'
if score.missed > 0:
    win_msg = f'Yeah you won!\nYou missed the ball {score.missed} time/times.'
    final_msg.write(win_msg, align='center', font=('Courier', 24, 'normal'))
screen.exitonclick()