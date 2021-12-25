import pygame
import random
import math
from pygame import mixer
import os, sys

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(APP_FOLDER)

# Initialise the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("background_trim.jpg")

running = True

#Background music
mixer.music.load("music.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Score
score_value = 0
font = pygame.font.Font("notes.ttf", 32)
textX = 10
textY = 10 

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

#Game Over Text
end_font = pygame.font.Font("notes.ttf", 64)

def game_over_text():
    over_text = end_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (300, 250))

# Player
playerImg = pygame.image.load("player.png")
playerX = 368
playerY = 526
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Monster
monsterImg = []
monsterX = []
monsterY = []
monsterX_change = []
monsterY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    monsterImg.append(pygame.image.load("monster" + str(i) + ".png"))
    monsterX.append(random.randint(0, 735))
    monsterY.append(random.randint(0, 300))
    monsterX_change.append(0.2)
    monsterY_change.append(0)

def monster(x, y, i):
    screen.blit(monsterImg[i], (x, y))

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 526
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(monsterX, monsterY, bulletX, bulletY):
    distance =  math.sqrt(math.pow((monsterX-bulletX),2) + math.pow(monsterY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False


# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_Sound = mixer.Sound("shot.wav")
                bullet_Sound.play()
                bulletX = playerX
                fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        if monsterY[i] > 450:
            for j in range(num_of_enemies):
                monsterY[j] = 2000
            game_over_text()
            break

        monsterX[i] += monsterX_change[i]
        if monsterX[i] <= 0:
            monsterX_change[i] *= -1
            monsterY[i] += 40
        elif monsterX[i] >= 736:
            monsterX_change[i] *= -1
            monsterY[i] += 10

        collision = isCollision(monsterX[i], monsterY[i], bulletX, bulletY)
        if collision:
            collision_Sound = mixer.Sound("collision2.wav")
            collision_Sound.play()
            bulletY = 526
            bullet_state = "ready"
            score_value += 1
            monsterX[i] = random.randint(0, 736)
            monsterY[i] = random.randint(0, 300)
        monster(monsterX[i], monsterY[i], i)

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 526

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()