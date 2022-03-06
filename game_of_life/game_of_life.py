import pygame
import random
import os, sys
import math

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(APP_FOLDER)

win_height = 1000
win_width = 1000
run = True
block_size = 10

pygame.init()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Game of Life')


class Cell(object):
    def __init__(self, x, y, state, colour, f_state):
        self.x = x
        self.y = y
        self.state = state
        self.colour = colour

def create_grid():
    grid = [[0 for x in range(100)] for x in range(100)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            r = 0
            g = 0
            b = random.randint(100,255)
            grid[i][j] = Cell(i, j, False, (r,g,b), False)

    return grid

def draw_mesh(window):
    x = 0
    y = 0

    for l in range(100):
        x = x + block_size
        y = y + block_size
        pygame.draw.line(window, (25,25,25), (x, 0), (x,win_width))
        pygame.draw.line(window, (25,25,25), (0, y), (win_width,y))

def draw_grid(window, grid):
    x = 0
    y = 0

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].state == True:
                pygame.draw.rect(window, grid[i][j].colour, (x + i * block_size, y + j * block_size, block_size, block_size))

def change_colour(grid, colour):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if colour == "r":
                grid[i][j].colour = (random.randint(100,255), 0, 0)
            if colour == "g":
                grid[i][j].colour = (0, random.randint(100,255), 0)
            if colour == "b":
                grid[i][j].colour = (0, 0, random.randint(100,255))

def liven_cells(grid, live_amount):
    amount = 0
    while amount < live_amount:
        i = random.randint(0, 99)
        j = random.randint(0, 99)
        grid[i][j].state = True
        amount = amount + 1
        
def iterate_lifecycle(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].f_state = check_life(grid, grid[i][j])
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].state = grid[i][j].f_state

def kill_all(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].state = False

def check_life(grid, cell):
    c = count_company(grid, cell)
    f_state = False
    if cell.state == True and c < 2: f_state = False
    if cell.state == True and (c == 2 or c == 3): f_state = cell.state
    if cell.state == True and c > 3: f_state = False
    if cell.state == False and c == 3: f_state = True
    return f_state

def count_company(grid, cell):
    x = cell.x
    y = cell.y
    neighbours = 0
    if not (x == 0):
        if not (y == 0):
            if grid[x-1][y-1].state == True: neighbours += 1
        if grid[x-1][y].state == True: neighbours += 1
        if not (y == 99):
            if grid[x-1][y+1].state == True: neighbours += 1

    if not (y == 0):
        if grid[x][y-1].state == True: neighbours += 1
    if not (y == 99):
        if grid[x][y+1].state == True: neighbours += 1

    if not (x == 99):
        if not (y == 0):
            if grid[x+1][y-1].state == True: neighbours += 1
        if grid[x+1][y].state == True: neighbours += 1
        if not (y == 99):
            if grid[x+1][y+1].state == True: neighbours += 1

    return neighbours


def display_window(window, grid):
    win.fill((0,0,0))
    draw_mesh(window)
    draw_grid(win, grid)
    pygame.display.update()

grid = create_grid()
step_time = 0
step_speed = 0.27
clock = pygame.time.Clock()
simulate = False

while run:
    step_time += clock.get_rawtime()
    clock.tick()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                    liven_cells(grid, 100)
            if event.key == pygame.K_m:
                    iterate_lifecycle(grid)
            if event.key == pygame.K_k:
                    kill_all(grid)
            if event.key == pygame.K_r:
                    colour = 'r'
                    change_colour(grid, colour)
            if event.key == pygame.K_g:
                    colour = 'g'
                    change_colour(grid, colour)
            if event.key == pygame.K_b:
                    colour = 'b'
                    change_colour(grid, colour)
            if event.key == pygame.K_SPACE:
                if simulate == False:
                    simulate = True
                else:
                    simulate = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x = int(math.floor(event.pos[0]/10))
            y = int(math.floor(event.pos[1]/10))
            if event.button == 1:
                if grid[x][y].state == True: grid[x][y].state = False
                else: grid[x][y].state = True
            if event.button == 3:
                print(str(count_company(grid, grid[x][y])))           

    if step_time / 1000 > step_speed and simulate == True:
        step_time = 0
        iterate_lifecycle(grid)

    display_window(win, grid)