import turtle
import winsound
import time

wn = turtle.Screen()
wn.title("Pong by Piotr")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a= turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("blue")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b= turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("red")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball= turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.1
ball.dy = 0.1

#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Speed
speed = turtle.Turtle()
speed.speed(0)
speed.color("white")
speed.penup()
speed.hideturtle()
speed.goto(-300, -260)
speed.write("Speed: 0.1", align="center", font=("Courier", 12, "normal"))

# Playground
line = turtle.Turtle()
line.speed(0)
line.shape("square")
line.color("grey")
line.penup()
line.goto(0, 0)
line.shapesize(stretch_len=0.01, stretch_wid=28)

circle = turtle.Turtle()
circle.color("grey")
circle.shape("circle")
circle.shapesize(0.05, 0.05)
circle.goto(0, -100)
circle.circle(100)
circle.penup()

# Function
def paddle_a_up():
    if paddle_a.ycor() < 230:
        y = paddle_a.ycor()
        y += 20
        paddle_a.sety(y)

def paddle_a_down():
    if paddle_a.ycor() > -230:
        y = paddle_a.ycor()
        y -= 20
        paddle_a.sety(y)

def paddle_b_up():
    if paddle_b.ycor() < 230:
        y = paddle_b.ycor()
        y += 20
        paddle_b.sety(y)

def paddle_b_down():
    if paddle_b.ycor() > -230:
        y = paddle_b.ycor()
        y -= 20
        paddle_b.sety(y)

def writeSpeed():
    speed.clear()
    speed.write("Speed: {}".format(abs(ball.dx)), align="center", font=("Courier", 12, "normal"))

def speed_up():
    ball.dx = round(ball.dx * 2, 2)
    ball.dy = round(ball.dy * 2, 2)
    writeSpeed()

def speed_down():
    ball.dx = round(ball.dx / 2, 2)
    ball.dy = round(ball.dy / 2, 2)
    writeSpeed()

def difficulty_up():
    ball.dx = round(ball.dx * 1.1, 2)
    ball.dy = round(ball.dy * 1.1, 2)
    writeSpeed()

def setup():
    i = 3
    ball.color("white")
    wn.update()
    while i > 0:
        start = turtle.Turtle()
        start.speed(0)
        start.color("green")
        start.penup()
        start.hideturtle()
        start.goto(0, 0)
        start.write("{}".format(i), align="center", font=("Courier", 56, "bold"))
        i -= 1
        time.sleep(0.5)
        start.clear()

def finish():
    turtle.bye()

# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")
wn.onkeypress(speed_up, "o")
wn.onkeypress(speed_down, "i")
wn.onkeypress(finish, "u")

#Main game loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #Border checking
    if ball.ycor() > 290:
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 380:
        winsound.PlaySound("loss.wav", winsound.SND_ASYNC)
        time.sleep(0.5)
        ball.goto(0,0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
        difficulty_up()
        setup()

    if ball.xcor() < -390:
        winsound.PlaySound("loss.wav", winsound.SND_ASYNC)
        time.sleep(0.5)
        ball.goto(0,0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
        difficulty_up()
        setup()

    # Paddle and ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350 and (ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50)):
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.color("coral")
        ball.setx(340)
        ball.dx *= -1

    if (ball.xcor() < -340 and ball.xcor() > -350 and (ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50)):
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.color("cornflowerblue")
        ball.setx(-340)
        ball.dx *= -1