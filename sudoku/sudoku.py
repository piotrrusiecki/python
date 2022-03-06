from asyncio.windows_events import NULL
from contextlib import nullcontext
from pickle import FALSE
from turtle import left
from typing import OrderedDict
import itertools
from xml.sax.handler import property_xml_string
import pygame
import pprint
import os, sys
import math
from collections import ChainMap, OrderedDict

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(APP_FOLDER)

win_height = 810
win_width = 1200
not_solved = True
block_size = 90
colour_pos = (50, 50, 50)
colour_sol = (0, 100, 100)
colour_sin = (100, 100, 0)
colour_hid = (0, 100, 0)
colour_row = (100, 0, 0)
colour_col = (0, 0, 100)
colour_cre = (75, 0, 0) 
colour_cgr = (0, 75, 0)
props = ['prop_1', 'prop_2', 'prop_3', 'prop_4', 'prop_5', 'prop_6', 'prop_7', 'prop_8', 'prop_9']
groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
rows = ["row_0", "row_1", "row_2", "row_3", "row_4", "row_5", "row_6", "row_7", "row_8"]
cols = ["col_0", "col_1", "col_2", "col_3", "col_4", "col_5", "col_6", "col_7", "col_8"]
grps = ["grp_A", "grp_B", "grp_C", "grp_D", "grp_E", "grp_F", "grp_G", "grp_H", "grp_I"]
pall = [(255,0,0), (225,0,0), (200,0,0), (175,0,0), (150,0,0), (125,0,0), (100,0,0), (75,0,0), (50,0,0)]
all_chains = {}

pygame.init()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Sudoku')

class Cell(object):
    def __init__(self, x, y, solved, value, group="Z"):
        self.x = x
        self.y = y
        self.c = int(x / block_size)
        self.r = int(y / block_size)
        self.loc = (str(self.c) + '/' + str(self.r))
        self.solved = False
        self.value = value
        self.group = group
        self.grp = None
        self.g = 0
        self.prop_1 = False
        self.prop_2 = False
        self.prop_3 = False
        self.prop_4 = False
        self.prop_5 = False
        self.prop_6 = False
        self.prop_7 = False
        self.prop_8 = False
        self.prop_9 = False
        self.prop_states = {"prop_1" : (None, "NON"), "prop_2" : (None, "NON"), "prop_3" : (None, "NON"), "prop_4" :  (None, "NON"), "prop_5" :  (None, "NON"), "prop_6" :  (None, "NON"), "prop_7" :  (None, "NON"), "prop_8" :  (None, "NON"), "prop_9" :  (None, "NON")}
        self.proplist = []
        self.chainnumber = 0
        self.chainstate = "NONE"
        self.solution = 0
        self.propcount = 0
    def genproplist(self):
        self.proplist = []
        if self.prop_1: self.proplist.append('prop_1')
        if self.prop_2: self.proplist.append('prop_2')
        if self.prop_3: self.proplist.append('prop_3')
        if self.prop_4: self.proplist.append('prop_4')
        if self.prop_5: self.proplist.append('prop_5')
        if self.prop_6: self.proplist.append('prop_6')
        if self.prop_7: self.proplist.append('prop_7')
        if self.prop_8: self.proplist.append('prop_8')
        if self.prop_9: self.proplist.append('prop_9')
    def updateprops(self):
        for prop in props:
            if prop in self.proplist:
                setattr(self, prop, True)
            elif prop not in self.proplist:
                setattr(self, prop, False)
    def __repr__(self):
        return (str(self.c) + '/' + str(self.r) + ': ' + str(self.proplist))
    def __str__(self):
        return (str(self.c) + '/' + str(self.r) + ': ' + str(self.proplist))
    def __lt__(self,other):
        this = self.y * 10 + self.x
        that = other.y * 10 + other.x
        return this < that
    def __le__(self,other):
        this = self.y * 10 + self.x
        that = other.y * 10 + other.x
        return this <= that
    def __gt__(self,other):
        this = self.y * 10 + self.x
        that = other.y * 10 + other.x
        return this > that	
    def __ge__(self,other):
        this = self.y * 10 + self.x
        that = other.y * 10 + other.x
        return this >= that

def create_grid():
    print('*)  Create grid')
    grid = [[0 for x in range(9)] for x in range(9)]
    x = 0
    y = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[i][j] = Cell(x + i * block_size, y + j * block_size, False, 0)
            if i <= 2 and j <= 2: 
                grid[i][j].group = "A"
                grid[i][j].grp = "grp_A"
                grid[i][j].g = 0
            elif i <= 5 and j <= 2: 
                grid[i][j].group = "B"
                grid[i][j].grp = "grp_B"
                grid[i][j].g = 1
            elif j <= 2: 
                grid[i][j].group = "C"
                grid[i][j].grp = "grp_C"
                grid[i][j].g = 2
            elif i <=2 and j > 2 and j <= 5: 
                grid[i][j].group = "D"
                grid[i][j].grp = "grp_D"
                grid[i][j].g = 3
            elif i <= 5 and j > 2 and j <= 5: 
                grid[i][j].group = "E"
                grid[i][j].grp = "grp_E"
                grid[i][j].g = 4
            elif j > 2 and j <= 5:
                grid[i][j].group = "F"
                grid[i][j].grp = "grp_F"
                grid[i][j].g = 5
            elif i <= 2 and j >=6: 
                grid[i][j].group = "G"
                grid[i][j].grp = "grp_G"
                grid[i][j].g = 6
            elif i <= 5 and j >= 6: 
                grid[i][j].group = "H"
                grid[i][j].grp = "grp_H"
                grid[i][j].g = 7
            elif j >= 6: 
                grid[i][j].group = "I"
                grid[i][j].grp = "grp_I"
                grid[i][j].g = 8
    return grid

def show_highlight(grid):
    print('*)  Highlight possible solutions (pale grey)')
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].solved == False:
                if grid[i][j].prop_1 == True: 
                    if grid[i][j].prop_states["prop_1"][1] == "NON": pygame.draw.rect(win, colour_pos, (grid[i][j].x, grid[i][j].y, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_1"][1] == "GRN": pygame.draw.rect(win, colour_cgr, (grid[i][j].x, grid[i][j].y, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_1"][1] == "RED": pygame.draw.rect(win, colour_cre, (grid[i][j].x, grid[i][j].y, block_size/3, block_size/3))
                if grid[i][j].prop_2 == True: 
                    if grid[i][j].prop_states["prop_2"][1] == "NON": pygame.draw.rect(win, colour_pos, (grid[i][j].x+30, grid[i][j].y, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_2"][1] == "GRN": pygame.draw.rect(win, colour_cgr, (grid[i][j].x+30, grid[i][j].y, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_2"][1] == "RED": pygame.draw.rect(win, colour_cre, (grid[i][j].x+30, grid[i][j].y, block_size/3, block_size/3))
                if grid[i][j].prop_3 == True: 
                    if grid[i][j].prop_states["prop_3"][1] == "NON": pygame.draw.rect(win, colour_pos, (grid[i][j].x+60, grid[i][j].y, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_3"][1] == "GRN": pygame.draw.rect(win, colour_cgr, (grid[i][j].x+60, grid[i][j].y, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_3"][1] == "RED": pygame.draw.rect(win, colour_cre, (grid[i][j].x+60, grid[i][j].y, block_size/3, block_size/3))
                if grid[i][j].prop_4 == True: 
                    if grid[i][j].prop_states["prop_4"][1] == "NON": pygame.draw.rect(win, colour_pos, (grid[i][j].x, grid[i][j].y+30, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_4"][1] == "GRN": pygame.draw.rect(win, colour_cgr, (grid[i][j].x, grid[i][j].y+30, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_4"][1] == "RED": pygame.draw.rect(win, colour_cre, (grid[i][j].x, grid[i][j].y+30, block_size/3, block_size/3))
                if grid[i][j].prop_5 == True: 
                    if grid[i][j].prop_states["prop_5"][1] == "NON": pygame.draw.rect(win, colour_pos, (grid[i][j].x+30, grid[i][j].y+30, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_5"][1] == "GRN": pygame.draw.rect(win, colour_cgr, (grid[i][j].x+30, grid[i][j].y+30, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_5"][1] == "RED": pygame.draw.rect(win, colour_cre, (grid[i][j].x+30, grid[i][j].y+30, block_size/3, block_size/3))
                if grid[i][j].prop_6 == True: 
                    if grid[i][j].prop_states["prop_6"][1] == "NON": pygame.draw.rect(win, colour_pos, (grid[i][j].x+60, grid[i][j].y+30, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_6"][1] == "GRN": pygame.draw.rect(win, colour_cgr, (grid[i][j].x+60, grid[i][j].y+30, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_6"][1] == "RED": pygame.draw.rect(win, colour_cre, (grid[i][j].x+60, grid[i][j].y+30, block_size/3, block_size/3))
                if grid[i][j].prop_7 == True: 
                    if grid[i][j].prop_states["prop_7"][1] == "NON": pygame.draw.rect(win, colour_pos, (grid[i][j].x, grid[i][j].y+60, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_7"][1] == "GRN": pygame.draw.rect(win, colour_cgr, (grid[i][j].x, grid[i][j].y+60, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_7"][1] == "RED": pygame.draw.rect(win, colour_cre, (grid[i][j].x, grid[i][j].y+60, block_size/3, block_size/3))
                if grid[i][j].prop_8 == True: 
                    if grid[i][j].prop_states["prop_8"][1] == "NON": pygame.draw.rect(win, colour_pos, (grid[i][j].x+30, grid[i][j].y+60, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_8"][1] == "GRN": pygame.draw.rect(win, colour_cgr, (grid[i][j].x+30, grid[i][j].y+60, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_8"][1] == "RED": pygame.draw.rect(win, colour_cre, (grid[i][j].x+30, grid[i][j].y+60, block_size/3, block_size/3))
                if grid[i][j].prop_9 == True: 
                    if grid[i][j].prop_states["prop_9"][1] == "NON": pygame.draw.rect(win, colour_pos, (grid[i][j].x+60, grid[i][j].y+60, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_9"][1] == "GRN": pygame.draw.rect(win, colour_cgr, (grid[i][j].x+60, grid[i][j].y+60, block_size/3, block_size/3))
                    if grid[i][j].prop_states["prop_9"][1] == "RED": pygame.draw.rect(win, colour_cre, (grid[i][j].x+60, grid[i][j].y+60, block_size/3, block_size/3))

                if grid[i][j].prop_1 == False: pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x, grid[i][j].y, block_size/3, block_size/3))
                if grid[i][j].prop_2 == False: pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+30, grid[i][j].y, block_size/3, block_size/3))
                if grid[i][j].prop_3 == False: pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+60, grid[i][j].y, block_size/3, block_size/3))
                if grid[i][j].prop_4 == False: pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x, grid[i][j].y+30, block_size/3, block_size/3))
                if grid[i][j].prop_5 == False: pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+30, grid[i][j].y+30, block_size/3, block_size/3))
                if grid[i][j].prop_6 == False: pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+60, grid[i][j].y+30, block_size/3, block_size/3))
                if grid[i][j].prop_7 == False: pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x, grid[i][j].y+60, block_size/3, block_size/3))
                if grid[i][j].prop_8 == False: pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+30, grid[i][j].y+60, block_size/3, block_size/3))
                if grid[i][j].prop_9 == False: pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+60, grid[i][j].y+60, block_size/3, block_size/3))

            if grid[i][j].solved == True:
                pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x, grid[i][j].y, block_size/3, block_size/3))
                pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+30, grid[i][j].y, block_size/3, block_size/3))
                pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+60, grid[i][j].y, block_size/3, block_size/3))
                pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x, grid[i][j].y+30, block_size/3, block_size/3))
                pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+30, grid[i][j].y+30, block_size/3, block_size/3))
                pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+60, grid[i][j].y+30, block_size/3, block_size/3))
                pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x, grid[i][j].y+60, block_size/3, block_size/3))
                pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+30, grid[i][j].y+60, block_size/3, block_size/3))
                pygame.draw.rect(win, (0, 0, 0), (grid[i][j].x+60, grid[i][j].y+60, block_size/3, block_size/3))
                grid[i][j].prop_1 = False
                grid[i][j].prop_2 = False
                grid[i][j].prop_3 = False
                grid[i][j].prop_4 = False
                grid[i][j].prop_5 = False
                grid[i][j].prop_6 = False
                grid[i][j].prop_7 = False
                grid[i][j].prop_8 = False
                grid[i][j].prop_9 = False
                for prop in props:
                    grid[i][j].prop_states[prop] = (None, "NON")
                    # if prop in grid[i][j].proplist: grid[i][i].proplist.remove(prop)
                if grid[i][j].value == 1: pygame.draw.rect(win, colour_sol, (grid[i][j].x, grid[i][j].y, block_size/3, block_size/3))
                if grid[i][j].value == 2: pygame.draw.rect(win, colour_sol, (grid[i][j].x+30, grid[i][j].y, block_size/3, block_size/3))
                if grid[i][j].value == 3: pygame.draw.rect(win, colour_sol, (grid[i][j].x+60, grid[i][j].y, block_size/3, block_size/3))
                if grid[i][j].value == 4: pygame.draw.rect(win, colour_sol, (grid[i][j].x, grid[i][j].y+30, block_size/3, block_size/3))
                if grid[i][j].value == 5: pygame.draw.rect(win, colour_sol, (grid[i][j].x+30, grid[i][j].y+30, block_size/3, block_size/3))
                if grid[i][j].value == 6: pygame.draw.rect(win, colour_sol, (grid[i][j].x+60, grid[i][j].y+30, block_size/3, block_size/3))
                if grid[i][j].value == 7: pygame.draw.rect(win, colour_sol, (grid[i][j].x, grid[i][j].y+60, block_size/3, block_size/3))
                if grid[i][j].value == 8: pygame.draw.rect(win, colour_sol, (grid[i][j].x+30, grid[i][j].y+60, block_size/3, block_size/3))
                if grid[i][j].value == 9: pygame.draw.rect(win, colour_sol, (grid[i][j].x+60, grid[i][j].y+60, block_size/3, block_size/3))
 
    for key in all_chains.keys():
        for i in range(len(all_chains[key])):
            for cell in range(len(all_chains[key][i])):
                draw_line(win, all_chains[key][i][cell][0], all_chains[key][i][cell][1], props[props.index(key)])

def large_text(surface, text, x, y):
    font = pygame.font.SysFont("comicsans", 60, bold=False)
    label = font.render (text, 1, (150,150,150))
    surface.blit(label, (x, y))

def write_numbers(surface, grid):
    print('*)  Write solution numbers')
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j].value == 1: large_text(surface, '1', grid[i][j].x+30, grid[i][j].y)
            if grid[i][j].value == 2: large_text(surface, '2', grid[i][j].x+30, grid[i][j].y)
            if grid[i][j].value == 3: large_text(surface, '3', grid[i][j].x+30, grid[i][j].y) 
            if grid[i][j].value == 4: large_text(surface, '4', grid[i][j].x+30, grid[i][j].y) 
            if grid[i][j].value == 5: large_text(surface, '5', grid[i][j].x+30, grid[i][j].y) 
            if grid[i][j].value == 6: large_text(surface, '6', grid[i][j].x+30, grid[i][j].y) 
            if grid[i][j].value == 7: large_text(surface, '7', grid[i][j].x+30, grid[i][j].y) 
            if grid[i][j].value == 8: large_text(surface, '8', grid[i][j].x+30, grid[i][j].y) 
            if grid[i][j].value == 9: large_text(surface, '9', grid[i][j].x+30, grid[i][j].y) 

def draw_mesh(window):
    print('*)  Draw mesh')
    x = 0
    y = 0

    for l in range(26):
        x = x + block_size/3
        y = y + block_size/3
        if l == 2 or l == 5 or l == 11 or l == 14 or l == 20 or l == 23:
            pygame.draw.line(window, (75,75,75), (x, 0), (x,win_width))
            pygame.draw.line(window, (75,75,75), (0, y), (810,y))
        elif l == 8 or l == 17:
            pygame.draw.line(window, (150,150,150), (x, 0), (x,win_width))
            pygame.draw.line(window, (150,150,150), (0, y), (810,y))
        else:
            pygame.draw.line(window, (25,25,25), (x, 0), (x,win_width))
            pygame.draw.line(window, (25,25,25), (0, y), (810,y))

def draw_line(win, cell_a, cell_b, prop):
    if props.index(prop) == 0:
        mod_x = -30
        mod_y = -30
    if props.index(prop) == 1:
        mod_x = 0
        mod_y = -30
    if props.index(prop) == 2: 
        mod_x = 30
        mod_y = -30
    if props.index(prop) == 3: 
        mod_x = -30
        mod_y = 0
    if props.index(prop) == 4: 
        mod_x = 0
        mod_y = 0
    if props.index(prop) == 5: 
        mod_x = 30
        mod_y = 0
    if props.index(prop) == 6: 
        mod_x = -30
        mod_y = 30
    if props.index(prop) == 7: 
        mod_x = 0
        mod_y = 30
    if props.index(prop) == 8: 
        mod_x = 30
        mod_y = 30

    cell_3 = block_size / 3
    cell_2 = block_size / 2
    lef = 0
    top = 0
    wid = 0
    hei = 0

    # Horizontal 
    if cell_a.x != cell_b.x and cell_a.y == cell_b.y:
        wid = abs(cell_a.x - cell_b.x)
        hei = cell_3

        if cell_a.x > cell_b.x: lef = cell_b.x + cell_2
        else: lef = cell_a.x + cell_2 + mod_x
        if cell_a.y > cell_b.y: top = cell_b.y + cell_3
        else: top = cell_a.y + cell_3 + mod_y
        pygame.draw.arc(win, pall[props.index(prop)], (lef, top, wid, hei), 0, 3.14, 2)

    # Vertical
    if cell_a.x == cell_b.x and cell_a.y != cell_b.y:
        wid = cell_3
        hei = abs(cell_a.y - cell_b.y)

        if cell_a.x > cell_b.x: lef = cell_b.x + cell_2
        else: lef = cell_a.x + cell_3 + mod_x
        if cell_a.y > cell_b.y: top = cell_b.y + cell_3
        else: top = cell_a.y + cell_2 + mod_y
        pygame.draw.arc(win, pall[props.index(prop)], (lef, top, wid, hei), 1.57, 4.71, 2)

    # Diagonal
    if cell_a.x != cell_b.x and cell_a.y != cell_b.y:
        hei = cell_3
        wid = math.sqrt(abs(cell_a.x - cell_b.x) ** 2 + abs(cell_a.y - cell_b.y) ** 2)
        
        if cell_a.x > cell_b.x: 
            lef = cell_b.x + cell_3 + mod_x
        else: 
            lef = cell_a.x + cell_3 + mod_x

        if cell_a.y > cell_b.y:
            top = cell_b.y + cell_2 + mod_y
        else:
            top = cell_a.y + cell_2 + mod_y

        diagonalSurf = pygame.Surface([wid, hei], pygame.SRCALPHA, 32)
        diagonalSurf = diagonalSurf.convert_alpha()

        pygame.draw.arc(diagonalSurf, pall[props.index(prop)], (0, 0, wid, hei), 0, 3.14, 2)
        rot = -1 * math.degrees(math.asin((cell_b.y-cell_a.y)/wid)) 

        diagonalSurf_rot = pygame.transform.rotate(diagonalSurf, rot)
        win.blit(diagonalSurf_rot, (lef,top))

def overall_check(grid):
    print('1)  Remove possibilities that are invalid')
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            remove_possibilities(grid, grid[i][j], i, j)
            grid[i][j].genproplist()

def remove_possibilities(grid, Cell, x, y):
    group = Cell.group
    for i in range(len(grid)):
        if Cell.value == 1:
            if grid[i][y].prop_1 and grid[i][y].solved == False:
                print('    Removing prop_1 in cell ' + str(i) + '/' + str(y) + ' as cell ' + str(x) + '/' + str(y) + ' has value 1')
                grid[i][y].prop_1 = False
            if grid[x][i].prop_1 and grid[x][i].solved == False:
                print('    Removing prop_1 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 1')
                grid[x][i].prop_1 = False
        if Cell.value == 2:
            if grid[i][y].prop_2 and grid[i][y].solved == False:
                print('    Removing prop_2 in cell ' + str(i) + '/' + str(y) + ' as cell ' + str(x) + '/' + str(y) + ' has value 2')
                grid[i][y].prop_2 = False
            if grid[x][i].prop_2 and grid[x][i].solved == False:
                print('    Removing prop_2 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 2')
                grid[x][i].prop_2 = False
        if Cell.value == 3:
            if grid[i][y].prop_3 and grid[i][y].solved == False:
                print('    Removing prop_3 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 3')
                grid[i][y].prop_3 = False
            if grid[x][i].prop_3 and grid[x][i].solved == False:
                print('    Removing prop_3 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 3')
                grid[x][i].prop_3 = False
        if Cell.value == 4:
            if grid[i][y].prop_4 and grid[i][y].solved == False:
                print('    Removing prop_4 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 4')
                grid[i][y].prop_4 = False
            if grid[x][i].prop_4 and grid[x][i].solved == False:
                print('    Removing prop_4 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 4')
                grid[x][i].prop_4 = False
        if Cell.value == 5:
            if grid[i][y].prop_5 and grid[i][y].solved == False:
                print('    Removing prop_5 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 5')
                grid[i][y].prop_5 = False
            if grid[x][i].prop_5 and grid[x][i].solved == False:
                print('    Removing prop_5 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 5')
                grid[x][i].prop_5 = False
        if Cell.value == 6:
            if grid[i][y].prop_6 and grid[i][y].solved == False:
                print('    Removing prop_6 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 6')
                grid[i][y].prop_6 = False
            if grid[x][i].prop_6 and grid[x][i].solved == False:
                print('    Removing prop_6 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 6')
                grid[x][i].prop_6 = False
        if Cell.value == 7:
            if grid[i][y].prop_7 and grid[i][y].solved == False:
                print('    Removing prop_7 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 7')
                grid[i][y].prop_7 = False
            if grid[x][i].prop_7 and grid[x][i].solved == False:
                print('    Removing prop_7 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 7')
                grid[x][i].prop_7 = False
        if Cell.value == 8:
            if grid[i][y].prop_8 and grid[i][y].solved == False:
                print('    Removing prop_8 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 8')
                grid[i][y].prop_8 = False
            if grid[x][i].prop_8 and grid[x][i].solved == False:
                print('    Removing prop_8 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 8')
                grid[x][i].prop_8 = False
        if Cell.value == 9:
            if grid[i][y].prop_9 and grid[i][y].solved == False:
                print('    Removing prop_9 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 9')
                grid[i][y].prop_9 = False
            if grid[x][i].prop_9 and grid[x][i].solved == False:
                print('    Removing prop_9 in cell ' + str(x) + '/' + str(i) + ' as cell ' + str(x) + '/' + str(y) + ' has value 9')
                grid[x][i].prop_9 = False
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].group == group:
                if Cell.value == 1:
                    if grid[i][j].prop_1 and grid[i][j].solved == False:
                        print('    Removing prop_1 in cell ' + str(i) + '/' + str(j) + ' as group ' + str(grid[i][j].group) + ' has value 1')
                        grid[i][j].prop_1 = False
                if Cell.value == 2:
                    if grid[i][j].prop_2 and grid[i][j].solved == False:
                        print('    Removing prop_1 in cell ' + str(i) + '/' + str(j) + ' as group ' + str(grid[i][j].group) + ' has value 2')
                        grid[i][j].prop_2 = False
                if Cell.value == 3:
                    if grid[i][j].prop_3 and grid[i][j].solved == False:
                        print('    Removing prop_1 in cell ' + str(i) + '/' + str(j) + ' as group ' + str(grid[i][j].group) + ' has value 3')
                        grid[i][j].prop_3 = False
                if Cell.value == 4:
                    if grid[i][j].prop_4 and grid[i][j].solved == False:
                        print('    Removing prop_1 in cell ' + str(i) + '/' + str(j) + ' as group ' + str(grid[i][j].group) + ' has value 4')
                        grid[i][j].prop_4 = False
                if Cell.value == 5:
                    if grid[i][j].prop_5 and grid[i][j].solved == False:
                        print('    Removing prop_1 in cell ' + str(i) + '/' + str(j) + ' as group ' + str(grid[i][j].group) + ' has value 5')
                        grid[i][j].prop_5 = False
                if Cell.value == 6:
                    if grid[i][j].prop_6 and grid[i][j].solved == False:
                        print('    Removing prop_1 in cell ' + str(i) + '/' + str(j) + ' as group ' + str(grid[i][j].group) + ' has value 6')
                        grid[i][j].prop_6 = False
                if Cell.value == 7:
                    if grid[i][j].prop_7 and grid[i][j].solved == False:
                        print('    Removing prop_1 in cell ' + str(i) + '/' + str(j) + ' as group ' + str(grid[i][j].group) + ' has value 7')
                        grid[i][j].prop_7 = False
                if Cell.value == 8:
                    if grid[i][j].prop_8 and grid[i][j].solved == False:
                        print('    Removing prop_1 in cell ' + str(i) + '/' + str(j) + ' as group ' + str(grid[i][j].group) + ' has value 8')
                        grid[i][j].prop_8 = False
                if Cell.value == 9:
                    if grid[i][j].prop_9 and grid[i][j].solved == False:
                        print('    Removing prop_1 in cell ' + str(i) + '/' + str(j) + ' as group ' + str(grid[i][j].group) + ' has value 9')
                        grid[i][j].prop_9 = False

def allow_setting_sol(grid, Cell, x, y):
    allow = True
    group = Cell.group

    for i in range(len(grid)):
        if i != y:
            if Cell.value == grid[x][i].value: allow = False
        if i != x:
            if Cell.value == grid[i][y].value: allow = False
        for j in range(len(grid[i])):
            if i != x and j != y:
                if grid[i][j].group == group:
                    if Cell.value == grid[i][j].value: allow = False
    return allow

def allow_setting_pos(grid, Cell, x, y):
    allow = True
    group = Cell.group

    for i in range(len(grid)):
        if i != y:
            if Cell.value == grid[x][i].value: allow = False
        if i != x:
            if Cell.value == grid[i][y].value: allow = False
        for j in range(len(grid[i])):
            if i != x and j != y:
                if grid[i][j].group == group:
                    if Cell.value == grid[i][j].value: allow = False
    return allow

def check_singles(grid):
# Looks for single possibility inside a cell
    print('*)  Highlight single solution in cell (dark yellow)')
    #This can be rewritten with single prop count and list of possibilities
    single = False
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            counter = 0
            if grid[i][j].prop_1 == True: counter += 1
            if grid[i][j].prop_2 == True: counter += 1
            if grid[i][j].prop_3 == True: counter += 1
            if grid[i][j].prop_4 == True: counter += 1
            if grid[i][j].prop_5 == True: counter += 1
            if grid[i][j].prop_6 == True: counter += 1
            if grid[i][j].prop_7 == True: counter += 1
            if grid[i][j].prop_8 == True: counter += 1
            if grid[i][j].prop_9 == True: counter += 1
            if counter == 1:
                if grid[i][j].prop_1 == True: pygame.draw.polygon(win, colour_sin, [(grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*1/6), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*1/3)])
                if grid[i][j].prop_2 == True: pygame.draw.polygon(win, colour_sin, [(grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*1/6), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*1/3)])
                if grid[i][j].prop_3 == True: pygame.draw.polygon(win, colour_sin, [(grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*1/6), (grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*1/3)])
                if grid[i][j].prop_4 == True: pygame.draw.polygon(win, colour_sin, [(grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*3/6), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*2/3)])
                if grid[i][j].prop_5 == True: pygame.draw.polygon(win, colour_sin, [(grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*3/6), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*2/3)])
                if grid[i][j].prop_6 == True: pygame.draw.polygon(win, colour_sin, [(grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*3/6), (grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*2/3)])
                if grid[i][j].prop_7 == True: pygame.draw.polygon(win, colour_sin, [(grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*5/6), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*3/3)])
                if grid[i][j].prop_8 == True: pygame.draw.polygon(win, colour_sin, [(grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*5/6), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*3/3)])
                if grid[i][j].prop_9 == True: pygame.draw.polygon(win, colour_sin, [(grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*5/6), (grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*3/3)])

def check_hidden_group(grid):
# Shows hidden (single) inside a cell group
    print('*)  Highlight single solution in group (dark green)')
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    for g in range(len(groups)):
        is_1 = 0
        is_2 = 0
        is_3 = 0
        is_4 = 0
        is_5 = 0
        is_6 = 0
        is_7 = 0
        is_8 = 0
        is_9 = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j].group == groups[g]:
                    if grid[i][j].prop_1 == True: is_1 +=1 
                    if grid[i][j].prop_2 == True: is_2 +=1
                    if grid[i][j].prop_3 == True: is_3 +=1
                    if grid[i][j].prop_4 == True: is_4 +=1
                    if grid[i][j].prop_5 == True: is_5 +=1
                    if grid[i][j].prop_6 == True: is_6 +=1
                    if grid[i][j].prop_7 == True: is_7 +=1
                    if grid[i][j].prop_8 == True: is_8 +=1
                    if grid[i][j].prop_9 == True: is_9 +=1
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j].group == groups[g]:
                    if is_1 == 1 and grid[i][j].prop_1 == True : pygame.draw.polygon(win, colour_hid, [(grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*1/6), (grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*1/3)])
                    if is_2 == 1 and grid[i][j].prop_2 == True : pygame.draw.polygon(win, colour_hid, [(grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*1/6), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*1/3)])         
                    if is_3 == 1 and grid[i][j].prop_3 == True : pygame.draw.polygon(win, colour_hid, [(grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*1/6), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*1/3)])         
                    if is_4 == 1 and grid[i][j].prop_4 == True : pygame.draw.polygon(win, colour_hid, [(grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*3/6), (grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*2/3)])         
                    if is_5 == 1 and grid[i][j].prop_5 == True : pygame.draw.polygon(win, colour_hid, [(grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*3/6), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*2/3)])         
                    if is_6 == 1 and grid[i][j].prop_6 == True : pygame.draw.polygon(win, colour_hid, [(grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*3/6), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*2/3)])         
                    if is_7 == 1 and grid[i][j].prop_7 == True : pygame.draw.polygon(win, colour_hid, [(grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*5/6), (grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*3/3)])         
                    if is_8 == 1 and grid[i][j].prop_8 == True : pygame.draw.polygon(win, colour_hid, [(grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*5/6), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*3/3)])        
                    if is_9 == 1 and grid[i][j].prop_9 == True : pygame.draw.polygon(win, colour_hid, [(grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*5/6), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*3/3)])        

def check_hidden_row(grid):
# Shows hidden (single) inside row of cells
    print('*)  Highlight single solution in row (dark red)')
    for j in range(len(grid)):
        is_1 = 0
        is_2 = 0
        is_3 = 0
        is_4 = 0
        is_5 = 0
        is_6 = 0
        is_7 = 0
        is_8 = 0
        is_9 = 0
        for i in range(len(grid[j])):
            if grid[i][j].prop_1 == True: is_1 +=1 
            if grid[i][j].prop_2 == True: is_2 +=1
            if grid[i][j].prop_3 == True: is_3 +=1
            if grid[i][j].prop_4 == True: is_4 +=1
            if grid[i][j].prop_5 == True: is_5 +=1
            if grid[i][j].prop_6 == True: is_6 +=1
            if grid[i][j].prop_7 == True: is_7 +=1
            if grid[i][j].prop_8 == True: is_8 +=1
            if grid[i][j].prop_9 == True: is_9 +=1
        for i in range(len(grid[j])):
            if is_1 == 1 and grid[i][j].prop_1 == True : pygame.draw.polygon(win, colour_row, [(grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*1/6), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*1/3)])
            if is_2 == 1 and grid[i][j].prop_2 == True : pygame.draw.polygon(win, colour_row, [(grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*1/6), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*1/3)])         
            if is_3 == 1 and grid[i][j].prop_3 == True : pygame.draw.polygon(win, colour_row, [(grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*1/6), (grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*1/3)])         
            if is_4 == 1 and grid[i][j].prop_4 == True : pygame.draw.polygon(win, colour_row, [(grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*3/6), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*2/3)])         
            if is_5 == 1 and grid[i][j].prop_5 == True : pygame.draw.polygon(win, colour_row, [(grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*3/6), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*2/3)])         
            if is_6 == 1 and grid[i][j].prop_6 == True : pygame.draw.polygon(win, colour_row, [(grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*3/6), (grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*2/3)])         
            if is_7 == 1 and grid[i][j].prop_7 == True : pygame.draw.polygon(win, colour_row, [(grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*5/6), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*3/3), (grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*3/3)])         
            if is_8 == 1 and grid[i][j].prop_8 == True : pygame.draw.polygon(win, colour_row, [(grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*5/6), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*3/3), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*3/3)])        
            if is_9 == 1 and grid[i][j].prop_9 == True : pygame.draw.polygon(win, colour_row, [(grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*5/6), (grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*3/3), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*3/3)])        

def check_hidden_column(grid):
# Shows hidden (single) inside a column of cells
    print('*)  Highlight single solution in column (dark blue)')
    for i in range(len(grid)):
        is_1 = 0
        is_2 = 0
        is_3 = 0
        is_4 = 0
        is_5 = 0
        is_6 = 0
        is_7 = 0
        is_8 = 0
        is_9 = 0
        for j in range(len(grid[i])):
            if grid[i][j].prop_1 == True: is_1 +=1 
            if grid[i][j].prop_2 == True: is_2 +=1
            if grid[i][j].prop_3 == True: is_3 +=1
            if grid[i][j].prop_4 == True: is_4 +=1
            if grid[i][j].prop_5 == True: is_5 +=1
            if grid[i][j].prop_6 == True: is_6 +=1
            if grid[i][j].prop_7 == True: is_7 +=1
            if grid[i][j].prop_8 == True: is_8 +=1
            if grid[i][j].prop_9 == True: is_9 +=1
        for j in range(len(grid[j])):
            if is_1 == 1 and grid[i][j].prop_1 == True : pygame.draw.polygon(win, colour_col, [(grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*1/6)])
            if is_2 == 1 and grid[i][j].prop_2 == True : pygame.draw.polygon(win, colour_col, [(grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*1/6)])         
            if is_3 == 1 and grid[i][j].prop_3 == True : pygame.draw.polygon(win, colour_col, [(grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*0/3), (grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*1/6)])         
            if is_4 == 1 and grid[i][j].prop_4 == True : pygame.draw.polygon(win, colour_col, [(grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*3/6)])         
            if is_5 == 1 and grid[i][j].prop_5 == True : pygame.draw.polygon(win, colour_col, [(grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*3/6)])         
            if is_6 == 1 and grid[i][j].prop_6 == True : pygame.draw.polygon(win, colour_col, [(grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*1/3), (grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*3/6)])         
            if is_7 == 1 and grid[i][j].prop_7 == True : pygame.draw.polygon(win, colour_col, [(grid[i][j].x+block_size*0/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*1/6, grid[i][j].y+block_size*5/6)])         
            if is_8 == 1 and grid[i][j].prop_8 == True : pygame.draw.polygon(win, colour_col, [(grid[i][j].x+block_size*1/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*3/6, grid[i][j].y+block_size*5/6)])        
            if is_9 == 1 and grid[i][j].prop_9 == True : pygame.draw.polygon(win, colour_col, [(grid[i][j].x+block_size*2/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*3/3, grid[i][j].y+block_size*2/3), (grid[i][j].x+block_size*5/6, grid[i][j].y+block_size*5/6)])        

def naked_pair_row(grid):
    print('2)  Checking for naked pair in row')
    for j in range(len(grid)):
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)):
            if grid[i][j].propcount == 2: paired_cells.append(grid[i][j])
        if len(paired_cells) >= 2:
            prop_sets = [set for set in itertools.combinations(props, 2)]
            cell_sets = [cell for cell in itertools.combinations(paired_cells, 2)]
            for prop_set in prop_sets:
                for cell_set in cell_sets:
                    if getattr(cell_set[0], prop_set[0]) == True and getattr(cell_set[1], prop_set[0]) == True and getattr(cell_set[0], prop_set[1]) == True and getattr(cell_set[1], prop_set[1]) == True:
                        print('    Found pair ' + str(cell_set[0]) + ' and ' + str(cell_set[1]) + ' with props ' + str(prop_set[0]) + ' and ' + str(prop_set[1]))
                        for i in range(len(grid)):
                            if i != cell_set[0].c and i != cell_set[1].c and getattr(grid[i][j], prop_set[0]) and not (grid[i][j].propcount == 2 and (getattr(grid[i][j], prop_set[0]) == True and getattr(grid[i][j], prop_set[1]) == True)):
                                print('       Removing ' + str(prop_set[0]) + ' in ' + str(i) + '/' + str(j))
                                setattr(grid[i][j], prop_set[0], False)
                            if i != cell_set[0].c and i != cell_set[1].c and getattr(grid[i][j], prop_set[1]) and not (grid[i][j].propcount == 2 and (getattr(grid[i][j], prop_set[0]) == True and getattr(grid[i][j], prop_set[1]) == True)):
                                print('       Removing ' + str(prop_set[1]) + ' in ' + str(i) + '/' + str(j))
                                setattr(grid[i][j], prop_set[1], False)

def naked_pair_column(grid):
    print('3)  Checking for naked pair in column')
    for i in range(len(grid)):
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for j in range(len(grid)):
            if grid[i][j].propcount == 2: paired_cells.append((i, j))
        if len(paired_cells) >= 2:
            prop_sets = [set for set in itertools.combinations(props, 2)]
            cell_sets = [cell for cell in itertools.combinations(paired_cells, 2)]
            for cell_set in cell_sets:
                for prop_set in prop_sets:
                    if getattr(grid[cell_set[0][0]][cell_set[0][1]], prop_set[0]) == True and getattr(grid[cell_set[1][0]][cell_set[1][1]], prop_set[0]) == True and getattr(grid[cell_set[0][0]][cell_set[0][1]], prop_set[1]) == True and getattr(grid[cell_set[1][0]][cell_set[1][1]], prop_set[1]) == True:
                        print('    Found pair' + str(cell_set[0]) + ' and ' + str(cell_set[1]) + ' with props ' + str(prop_set[0]) + ' and ' + str(prop_set[1]))
                        for j in range(len(grid)):
                            if j != cell_set[0][1] and j != cell_set[1][1] and getattr(grid[i][j], prop_set[0]) and not (grid[i][j].propcount == 2 and (getattr(grid[i][j], prop_set[0]) == True and getattr(grid[i][j], prop_set[1]) == True)):
                                print('       Removing ' + str(prop_set[0]) + ' in ' + str(i) + '/' + str(j))
                                setattr(grid[i][j], prop_set[0], False)
                            if j != cell_set[0][1] and j != cell_set[1][1] and getattr(grid[i][j], prop_set[1]) and not (grid[i][j].propcount == 2 and (getattr(grid[i][j], prop_set[0]) == True and getattr(grid[i][j], prop_set[1]) == True)):
                                print('       Removing ' + str(prop_set[1]) + ' in ' + str(i) + '/' + str(j))
                                setattr(grid[i][j], prop_set[1], False)

def naked_pair_group(grid):
    print('4)  Checking for naked pair in group')
    for g in groups:
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)): 
            for j in range(len(grid)):
                if grid[i][j].propcount == 2 and grid[i][j].group == g: paired_cells.append((i, j))
        if len(paired_cells) >= 2:
            prop_sets = [set for set in itertools.combinations(props, 2)]
            cell_sets = [cell for cell in itertools.combinations(paired_cells, 2)]
            for cell_set in cell_sets:
                for prop_set in prop_sets:
                    if getattr(grid[cell_set[0][0]][cell_set[0][1]], prop_set[0]) == True and getattr(grid[cell_set[1][0]][cell_set[1][1]], prop_set[0]) == True and getattr(grid[cell_set[0][0]][cell_set[0][1]], prop_set[1]) == True and getattr(grid[cell_set[1][0]][cell_set[1][1]], prop_set[1]) == True and grid[cell_set[0][0]][cell_set[0][1]].group == g and grid[cell_set[1][0]][cell_set[1][1]].group == g:
                        print('    Found pair ' + str(cell_set[0]) + ' and ' + str(cell_set[1]) + ' with props ' + str(prop_set[0]) + ' and ' + str(prop_set[1]))
                        for i in range(len(grid)):
                            for j in range(len(grid)):
                                if not (i == cell_set[0][0] and j == cell_set[0][1]) and not (i == cell_set[1][0] and j == cell_set[1][1]) and getattr(grid[i][j], prop_set[0]) and grid[i][j].group == g and not (grid[i][j].propcount == 2 and (getattr(grid[i][j], prop_set[0]) == True and getattr(grid[i][j], prop_set[1]) == True)):
                                    print('       Removing ' + str(prop_set[0]) + ' in ' + str(i) + '/' + str(j))
                                    setattr(grid[i][j], prop_set[0], False)
                                if not (i == cell_set[0][0] and j == cell_set[0][1]) and not (i == cell_set[1][0] and j == cell_set[1][1]) and getattr(grid[i][j], prop_set[1]) and grid[i][j].group == g and not (grid[i][j].propcount == 2 and (getattr(grid[i][j], prop_set[0]) == True and getattr(grid[i][j], prop_set[1]) == True)):
                                    print('       Removing ' + str(prop_set[1]) + ' in ' + str(i) + '/' + str(j))
                                    setattr(grid[i][j], prop_set[1], False)

def naked_triple_row(grid):
    print('5)  Checking for naked triple in row')
    for j in range(len(grid)):
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid[j])):
            if grid[i][j].propcount == 2 or grid[i][j].propcount == 3: paired_cells.append((grid[i][j]))
        if len(paired_cells) >= 3:
            prop_sets = [set for set in itertools.combinations(props, 3)]
            cell_sets = [cell for cell in itertools.combinations(paired_cells, 3)]
            for cell_set in cell_sets:
                for prop_set in prop_sets:
                    if set(cell_set[0].proplist).issubset(set(prop_set)) and \
                       set(cell_set[1].proplist).issubset(set(prop_set)) and \
                       set(cell_set[2].proplist).issubset(set(prop_set)) and \
                       any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0])]) and \
                       any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1])]) and \
                       any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2])]):
                        print('    Props: ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ', ' + str(prop_set[2]) + \
                              ' found in cells:\n      ' + cell_set[0].loc + ': ' + str(cell_set[0].proplist) + ',\n      ' + \
                              cell_set[1].loc + ': ' + str(cell_set[1].proplist) + ' and\n      ' + cell_set[2].loc + ': ' + \
                              str(cell_set[2].proplist))
                        for i in range(len(grid)):
                            if i != cell_set[0].c and i != cell_set[1].c and i != cell_set[2].c and not (grid[i][j].propcount <= 3 and set(grid[i][j].proplist).issubset(set(prop_set))):
                                if getattr(grid[i][j], prop_set[0]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[0]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[0], False)
                                if getattr(grid[i][j], prop_set[1]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[1]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[1], False)
                                if getattr(grid[i][j], prop_set[2]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[2]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[2], False)

def naked_triple_column(grid):
    print('6)  Checking for naked triple in column')
    for i in range(len(grid)):
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for j in range(len(grid)):
            if grid[i][j].propcount == 2 or grid[i][j].propcount == 3: paired_cells.append((grid[i][j]))
        if len(paired_cells) >= 3:
            prop_sets = [set for set in itertools.combinations(props, 3)]
            cell_sets = [cell for cell in itertools.combinations(paired_cells, 3)]
            for cell_set in cell_sets:
                for prop_set in prop_sets:
                    if set(cell_set[0].proplist).issubset(set(prop_set)) and \
                       set(cell_set[1].proplist).issubset(set(prop_set)) and \
                       set(cell_set[2].proplist).issubset(set(prop_set)) and \
                       any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0])]) and \
                       any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1])]) and \
                       any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2])]):
                        print('    Props: ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ', ' + str(prop_set[2]) + \
                              ' found in cells:\n      ' + cell_set[0].loc + ': ' + str(cell_set[0].proplist) + ',\n      ' + \
                              cell_set[1].loc + ': ' + str(cell_set[1].proplist) + ' and\n      ' + cell_set[2].loc + ': ' + \
                              str(cell_set[2].proplist))
                        for j in range(len(grid)):
                            if j != cell_set[0].r and j != cell_set[1].r and j != cell_set[2].r and not (grid[i][j].propcount <= 3 and set(grid[i][j].proplist).issubset(set(prop_set))):
                                if getattr(grid[i][j], prop_set[0]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[0]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[0], False)
                                if getattr(grid[i][j], prop_set[1]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[1]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[1], False)
                                if getattr(grid[i][j], prop_set[2]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[2]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[2], False)

def naked_triple_group(grid):
    print('7)  Checking for naked triple in group')
    for g in groups:
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if ( grid[i][j].propcount == 2 or grid[i][j].propcount == 3 ) and grid[i][j].group == g: paired_cells.append((grid[i][j]))
        if len(paired_cells) >= 3:
            prop_sets = [set for set in itertools.combinations(props, 3)]
            cell_sets = [cell for cell in itertools.combinations(paired_cells, 3)]
            for cell_set in cell_sets:
                for prop_set in prop_sets:
                    if set(cell_set[0].proplist).issubset(set(prop_set)) and \
                       set(cell_set[1].proplist).issubset(set(prop_set)) and \
                       set(cell_set[2].proplist).issubset(set(prop_set)) and \
                       any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0])]) and \
                       any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1])]) and \
                       any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2])]):
                        print('    Props: ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ', ' + str(prop_set[2]) + \
                              ' found in cells:\n      ' + cell_set[0].loc + ': ' + str(cell_set[0].proplist) + ',\n      ' + \
                              cell_set[1].loc + ': ' + str(cell_set[1].proplist) + ' and\n      ' + cell_set[2].loc + ': ' + \
                              str(cell_set[2].proplist) + ' in group ' + g)
                        for i in range(len(grid)):
                            for j in range(len(grid)):
                                if grid[i][j] != cell_set[0] and grid[i][j] != cell_set[1] and grid[i][j] != cell_set[2] and grid[i][j].group == g and not (grid[i][j].propcount <= 3 and set(grid[i][j].proplist).issubset(set(prop_set))):
                                    if getattr(grid[i][j], prop_set[0]) and grid[i][j].solved == False:
                                        print('       Removing ' + str(prop_set[0]) + ' from cell ' + str(grid[i][j].loc))
                                        setattr(grid[i][j], prop_set[0], False)
                                    if getattr(grid[i][j], prop_set[1]) and grid[i][j].solved == False:
                                        print('       Removing ' + str(prop_set[1]) + ' from cell ' + str(grid[i][j].loc))
                                        setattr(grid[i][j], prop_set[1], False)
                                    if getattr(grid[i][j], prop_set[2]) and grid[i][j].solved == False:
                                        print('       Removing ' + str(prop_set[2]) + ' from cell ' + str(grid[i][j].loc))
                                        setattr(grid[i][j], prop_set[2], False)

def naked_quad_row(grid):
    print('8)  Checking for naked quad in row')
    for j in range(len(grid)):
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid[j])):
            if grid[i][j].propcount >= 2 and grid[i][j].propcount <= 4: paired_cells.append((grid[i][j]))
        if len(paired_cells) >= 4:
            prop_sets = [set for set in itertools.combinations(props, 4)]
            cell_sets = [cell for cell in itertools.combinations(paired_cells, 4)]
            for cell_set in cell_sets:
                for prop_set in prop_sets:
                    if set(cell_set[0].proplist).issubset(set(prop_set)) and \
                       set(cell_set[1].proplist).issubset(set(prop_set)) and \
                       set(cell_set[2].proplist).issubset(set(prop_set)) and \
                       set(cell_set[3].proplist).issubset(set(prop_set)) and \
                       any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0]), getattr(cell_set[3], prop_set[0])]) and \
                       any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1]), getattr(cell_set[3], prop_set[1])]) and \
                       any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2]), getattr(cell_set[3], prop_set[2])]) and \
                       any([getattr(cell_set[0], prop_set[3]), getattr(cell_set[1], prop_set[3]), getattr(cell_set[2], prop_set[3]), getattr(cell_set[3], prop_set[3])]):
                        print('    Props: ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ', ' + str(prop_set[2]) + ', ' + str(prop_set[3]) + ' found in cells:\n      ' + \
                              cell_set[0].loc + ': ' + str(cell_set[0].proplist) + ',\n      ' + cell_set[1].loc + ': ' + str(cell_set[1].proplist) + ',\n      ' + cell_set[2].loc + \
                              ': ' + str(cell_set[2].proplist) + ' and\n      ' + cell_set[3].loc + ': ' + str(cell_set[3].proplist))
                        for i in range(len(grid)):
                            if i != cell_set[0].c and i != cell_set[1].c and i != cell_set[2].c  and i != cell_set[3].c and not (grid[i][j].propcount <= 4 and set(grid[i][j].proplist).issubset(set(prop_set))):
                                if getattr(grid[i][j], prop_set[0]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[0]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[0], False)
                                if getattr(grid[i][j], prop_set[1]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[1]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[1], False)
                                if getattr(grid[i][j], prop_set[2]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[2]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[2], False)
                                if getattr(grid[i][j], prop_set[3]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[3]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[3], False)

def naked_quad_column(grid):
    print('9)  Checking for naked quad in column')
    for i in range(len(grid)):
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for j in range(len(grid)):
            if grid[i][j].propcount >= 2 and grid[i][j].propcount <= 4: paired_cells.append((grid[i][j]))
        if len(paired_cells) >= 4:
            prop_sets = [set for set in itertools.combinations(props, 4)]
            cell_sets = [cell for cell in itertools.combinations(paired_cells, 4)]
            for cell_set in cell_sets:
                for prop_set in prop_sets:
                    if set(cell_set[0].proplist).issubset(set(prop_set)) and \
                       set(cell_set[1].proplist).issubset(set(prop_set)) and \
                       set(cell_set[2].proplist).issubset(set(prop_set)) and \
                       set(cell_set[3].proplist).issubset(set(prop_set)) and \
                       any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0]), getattr(cell_set[3], prop_set[0])]) and \
                       any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1]), getattr(cell_set[3], prop_set[1])]) and \
                       any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2]), getattr(cell_set[3], prop_set[2])]) and \
                       any([getattr(cell_set[0], prop_set[3]), getattr(cell_set[1], prop_set[3]), getattr(cell_set[2], prop_set[3]), getattr(cell_set[3], prop_set[3])]):
                        print('    Props: ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ', ' + str(prop_set[2]) + ', ' + str(prop_set[3]) + ' found in cells:\n      ' + \
                              cell_set[0].loc + ': ' + str(cell_set[0].proplist) + ',\n      ' + cell_set[1].loc + ': ' + str(cell_set[1].proplist) + ',\n      ' + cell_set[2].loc + \
                              ': ' + str(cell_set[2].proplist) + ' and\n      ' + cell_set[3].loc + ': ' + str(cell_set[3].proplist))
                        for j in range(len(grid)):
                            if j != cell_set[0].r and j != cell_set[1].r and j != cell_set[2].r  and j != cell_set[3].r and not (grid[i][j].propcount <= 4 and set(grid[i][j].proplist).issubset(set(prop_set))):
                                if getattr(grid[i][j], prop_set[0]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[0]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[0], False)
                                if getattr(grid[i][j], prop_set[1]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[1]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[1], False)
                                if getattr(grid[i][j], prop_set[2]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[2]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[2], False)
                                if getattr(grid[i][j], prop_set[3]) and grid[i][j].solved == False:
                                    print('       Removing ' + str(prop_set[3]) + ' from cell ' + str(grid[i][j].loc))
                                    setattr(grid[i][j], prop_set[3], False)

def naked_quad_group(grid):
    print('10) Checking for naked quad in group')
    for g in groups:
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if (grid[i][j].propcount >= 2 and grid[i][j].propcount <= 4) and grid[i][j].group == g: paired_cells.append((grid[i][j]))
        if len(paired_cells) >= 4:
            prop_sets = [set for set in itertools.combinations(props, 4)]
            cell_sets = [cell for cell in itertools.combinations(paired_cells, 4)]
            for cell_set in cell_sets:
                for prop_set in prop_sets:
                    if set(cell_set[0].proplist).issubset(set(prop_set)) and \
                    set(cell_set[1].proplist).issubset(set(prop_set)) and \
                    set(cell_set[2].proplist).issubset(set(prop_set)) and \
                    set(cell_set[3].proplist).issubset(set(prop_set)) and \
                    any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0]), getattr(cell_set[3], prop_set[0])]) and \
                    any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1]), getattr(cell_set[3], prop_set[1])]) and \
                    any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2]), getattr(cell_set[3], prop_set[2])]) and \
                    any([getattr(cell_set[0], prop_set[3]), getattr(cell_set[1], prop_set[3]), getattr(cell_set[2], prop_set[3]), getattr(cell_set[3], prop_set[3])]):
                        print('    Props: ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ', ' + str(prop_set[2]) + ', ' + str(prop_set[3]) + ' found in cells: \n      ' + \
                            cell_set[0].loc + ': ' + str(cell_set[0].proplist) + ',\n      ' + cell_set[1].loc + ': ' + str(cell_set[1].proplist) + ',\n      ' + cell_set[2].loc + \
                            ': ' + str(cell_set[2].proplist) + ' and\n      ' + cell_set[3].loc + ': ' + str(cell_set[3].proplist) + ' in group ' + g)
                        for i in range(len(grid)):
                            for j in range(len(grid)):
                                if grid[i][j] != cell_set[0] and grid[i][j] != cell_set[1] and grid[i][j] != cell_set[2] and grid[i][j] != cell_set[3] and not (grid[i][j].propcount <= 4 and set(grid[i][j].proplist).issubset(set(prop_set))) and grid[i][j].group == g:
                                    if getattr(grid[i][j], prop_set[0]) and grid[i][j].solved == False:
                                        print('       Removing ' + str(prop_set[0]) + ' from cell ' + str(grid[i][j].loc))
                                        setattr(grid[i][j], prop_set[0], False)
                                    if getattr(grid[i][j], prop_set[1]) and grid[i][j].solved == False:
                                        print('       Removing ' + str(prop_set[1]) + ' from cell ' + str(grid[i][j].loc))
                                        setattr(grid[i][j], prop_set[1], False)
                                    if getattr(grid[i][j], prop_set[2]) and grid[i][j].solved == False:
                                        print('       Removing ' + str(prop_set[2]) + ' from cell ' + str(grid[i][j].loc))
                                        setattr(grid[i][j], prop_set[2], False)
                                    if getattr(grid[i][j], prop_set[3]) and grid[i][j].solved == False:
                                        print('       Removing ' + str(prop_set[3]) + ' from cell ' + str(grid[i][j].loc))
                                        setattr(grid[i][j], prop_set[3], False)

def hidden_pair_row(grid):
    print("11) Checking for hidden pair in row")
    for j in range(len(grid)):
        props_counts = { "prop_1" : 0, "prop_2" : 0, "prop_3" : 0, "prop_4" : 0, "prop_5" : 0, "prop_6" : 0, "prop_7" : 0, "prop_8" : 0, "prop_9" : 0}
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)):
            if grid[i][j].propcount > 2: paired_cells.append((grid[i][j]))
            for prop in props:
                if getattr(grid[i][j], prop):
                    props_counts[prop] += 1
        if len(paired_cells) >= 2:
            prop_sets = [set for set in itertools.combinations(props, 2)]
            cell_sets = [set for set in itertools.combinations(paired_cells, 2)]
            for prop_set in prop_sets: 
                if props_counts[prop_set[0]] == 2 and props_counts[prop_set[1]] == 2:
                    for cell_set in cell_sets:
                        if getattr(cell_set[0], prop_set[0]) and getattr(cell_set[0], prop_set[1]) and getattr(cell_set[1], prop_set[0]) and getattr(cell_set[1], prop_set[1]) and cell_set[0].proplist != cell_set[1].proplist:
                            print('    Prop set ' + str(prop_set[0]) + ' and ' + str(prop_set[1]) + ' is a hidden pair in cell:\n    ' + str(cell_set[0]) + ' and cell:\n    ' + str(cell_set[1]) + ' in row ' + str(j)) 
                            for prop in props:
                                if prop != prop_set[0] and prop != prop_set[1] and getattr(cell_set[0], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[0].loc))
                                    setattr(cell_set[0], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and getattr(cell_set[1], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[1].loc))
                                    setattr(cell_set[1], prop, False)

def hidden_pair_column(grid):
    print("12) Checking for hidden pair in column")
    for i in range(len(grid)):
        props_counts = { "prop_1" : 0, "prop_2" : 0, "prop_3" : 0, "prop_4" : 0, "prop_5" : 0, "prop_6" : 0, "prop_7" : 0, "prop_8" : 0, "prop_9" : 0}
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for j in range(len(grid)):
            if grid[i][j].propcount > 2: paired_cells.append((grid[i][j]))
            for prop in props:
                if getattr(grid[i][j], prop):
                    props_counts[prop] += 1
        if len(paired_cells) >= 2:
            prop_sets = [set for set in itertools.combinations(props, 2)]
            cell_sets = [set for set in itertools.combinations(paired_cells, 2)]
            for prop_set in prop_sets: 
                if props_counts[prop_set[0]] == 2 and props_counts[prop_set[1]] == 2: 
                    for cell_set in cell_sets:
                        if getattr(cell_set[0], prop_set[0]) and getattr(cell_set[0], prop_set[1]) and getattr(cell_set[1], prop_set[0]) and getattr(cell_set[1], prop_set[1]) and cell_set[0].proplist != cell_set[1].proplist:
                            print('    Prop set ' + str(prop_set[0]) + ' and ' + str(prop_set[1]) + ' is a hidden pair in cell:\n    ' + str(cell_set[0]) + ' and cell:\n    ' + str(cell_set[1]) + ' in row ' + str(j)) 
                            for prop in props:
                                if prop != prop_set[0] and prop != prop_set[1] and getattr(cell_set[0], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[0].loc))
                                    setattr(cell_set[0], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and getattr(cell_set[1], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[1].loc))
                                    setattr(cell_set[1], prop, False)

def hidden_pair_group(grid):
    print("13) Checking for hidden pair in group")
    for g in groups:
        props_counts = { "prop_1" : 0, "prop_2" : 0, "prop_3" : 0, "prop_4" : 0, "prop_5" : 0, "prop_6" : 0, "prop_7" : 0, "prop_8" : 0, "prop_9" : 0}
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j].propcount > 2 and grid[i][j].group == g: paired_cells.append((grid[i][j]))
                for prop in props:
                    if getattr(grid[i][j], prop) and grid[i][j].group == g:
                        props_counts[prop] += 1
        if len(paired_cells) >= 2:
            prop_sets = [set for set in itertools.combinations(props, 2)]
            cell_sets = [set for set in itertools.combinations(paired_cells, 2)]
            for prop_set in prop_sets: 
                if props_counts[prop_set[0]] == 2 and props_counts[prop_set[1]] == 2: 
                    for cell_set in cell_sets:
                        if getattr(cell_set[0], prop_set[0]) and getattr(cell_set[0], prop_set[1]) and getattr(cell_set[1], prop_set[0]) and getattr(cell_set[1], prop_set[1]) and cell_set[0].proplist != cell_set[1].proplist:
                            print('    Prop set ' + str(prop_set[0]) + ' and ' + str(prop_set[1]) + ' is a hidden pair in cell:\n    ' + str(cell_set[0]) + ' and cell:\n    ' + str(cell_set[1]) + ' in group ' + str(g)) 
                            for prop in props:
                                if prop != prop_set[0] and prop != prop_set[1] and getattr(cell_set[0], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[0].loc))
                                    setattr(cell_set[0], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and getattr(cell_set[1], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[1].loc))
                                    setattr(cell_set[1], prop, False)

def hidden_triple_row(grid):
    print("14) Checking for hidden triple in row")
    for j in range(len(grid)):
        props_counts = { "prop_1" : 0, "prop_2" : 0, "prop_3" : 0, "prop_4" : 0, "prop_5" : 0, "prop_6" : 0, "prop_7" : 0, "prop_8" : 0, "prop_9" : 0}
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)):
            if grid[i][j].propcount > 3 : paired_cells.append((grid[i][j]))
            for prop in props:
                if getattr(grid[i][j], prop):
                    props_counts[prop] += 1
        prop_sets = [set for set in itertools.combinations(props, 3)]
        cell_sets = [set for set in itertools.combinations(paired_cells, 3)]
        if len(paired_cells) >= 3:
            for prop_set in prop_sets: 
                if (props_counts[prop_set[0]] == 2 or props_counts[prop_set[0]] == 3) and (props_counts[prop_set[1]] == 2 or props_counts[prop_set[1]] == 3) and (props_counts[prop_set[2]] == 2 or props_counts[prop_set[2]] == 3): 
                    for cell_set in cell_sets:
                        if set(prop_set).issubset(set(cell_set[0].proplist)) and \
                        set(prop_set).issubset(set(cell_set[1].proplist)) and \
                        set(prop_set).issubset(set(cell_set[2].proplist)) and \
                        any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0])]) and \
                        any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1])]) and \
                        any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2])]) and \
                        cell_set[0].proplist != cell_set[1].proplist and cell_set[0].proplist != cell_set[2].proplist and cell_set[1].proplist != cell_set[2].proplist:
                            print('    Prop set ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ' and ' + str(prop_set[2]) + ' is a hidden pair in cell:\n    ' + str(cell_set[0]) + ' and cell:\n    ' + str(cell_set[1]) + ' in row ' + str(j)) 
                            for prop in props:
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and getattr(cell_set[0], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[0].loc))
                                    setattr(cell_set[0], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and getattr(cell_set[1], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[1].loc))
                                    setattr(cell_set[1], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and getattr(cell_set[2], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[2].loc))
                                    setattr(cell_set[2], prop, False)

def hidden_triple_column(grid):
    print("15) Checking for hidden triple in column")
    for i in range(len(grid)):
        props_counts = { "prop_1" : 0, "prop_2" : 0, "prop_3" : 0, "prop_4" : 0, "prop_5" : 0, "prop_6" : 0, "prop_7" : 0, "prop_8" : 0, "prop_9" : 0}
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for j in range(len(grid)):
            if grid[i][j].propcount > 3 : paired_cells.append((grid[i][j]))
            for prop in props:
                if getattr(grid[i][j], prop):
                    props_counts[prop] += 1
        if len(paired_cells) >= 3:
            prop_sets = [set for set in itertools.combinations(props, 3)]
            cell_sets = [set for set in itertools.combinations(paired_cells, 3)]
            for prop_set in prop_sets: 
                if (props_counts[prop_set[0]] == 2 or props_counts[prop_set[0]] == 3) and (props_counts[prop_set[1]] == 2 or props_counts[prop_set[1]] == 3) and (props_counts[prop_set[2]] == 2 or props_counts[prop_set[2]] == 3): 
                    for cell_set in cell_sets:
                        if set(prop_set).issubset(set(cell_set[0].proplist)) and \
                        set(prop_set).issubset(set(cell_set[1].proplist)) and \
                        set(prop_set).issubset(set(cell_set[2].proplist)) and \
                        any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0])]) and \
                        any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1])]) and \
                        any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2])]) and \
                        cell_set[0].proplist != cell_set[1].proplist and cell_set[0].proplist != cell_set[2].proplist and cell_set[1].proplist != cell_set[2].proplist:
                            print('    Prop set ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ' and ' + str(prop_set[2]) + ' is a hidden pair in cell:\n    ' + str(cell_set[0]) + ' and cell:\n    ' + str(cell_set[1]) + ' in row ' + str(j)) 
                            for prop in props:
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and getattr(cell_set[0], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[0].loc))
                                    setattr(cell_set[0], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and getattr(cell_set[1], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[1].loc))
                                    setattr(cell_set[1], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and getattr(cell_set[2], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[2].loc))
                                    setattr(cell_set[2], prop, False)

def hidden_triple_group(grid):
    print("16) Checking for hidden triple in group")
    for g in groups:
        props_counts = { "prop_1" : 0, "prop_2" : 0, "prop_3" : 0, "prop_4" : 0, "prop_5" : 0, "prop_6" : 0, "prop_7" : 0, "prop_8" : 0, "prop_9" : 0}
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j].propcount > 3  and grid[i][j].group == g: paired_cells.append((grid[i][j]))
                for prop in props:
                    if getattr(grid[i][j], prop) and grid[i][j].group == g:
                        props_counts[prop] += 1
        if len(paired_cells) >= 3:
            prop_sets = [set for set in itertools.combinations(props, 3)]
            cell_sets = [set for set in itertools.combinations(paired_cells, 3)]
            for prop_set in prop_sets: 
                if (props_counts[prop_set[0]] == 2 or props_counts[prop_set[0]] == 3) and (props_counts[prop_set[1]] == 2 or props_counts[prop_set[1]] == 3) and (props_counts[prop_set[2]] == 2 or props_counts[prop_set[2]] == 3): 
                    for cell_set in cell_sets:
                        if set(prop_set).issubset(set(cell_set[0].proplist)) and \
                        set(prop_set).issubset(set(cell_set[1].proplist)) and \
                        set(prop_set).issubset(set(cell_set[2].proplist)) and \
                        any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0])]) and \
                        any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1])]) and \
                        any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2])]) and \
                        cell_set[0].proplist != cell_set[1].proplist and cell_set[0].proplist != cell_set[2].proplist and cell_set[1].proplist != cell_set[2].proplist:
                            print('    Prop set ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ' and ' + str(prop_set[2]) + ' is a hidden pair in cell:\n    ' + str(cell_set[0]) + ' and cell:\n    ' + str(cell_set[1]) + ' in group ' + str(g)) 
                            for prop in props:
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and getattr(cell_set[0], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[0].loc))
                                    setattr(cell_set[0], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and getattr(cell_set[1], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[1].loc))
                                    setattr(cell_set[1], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and getattr(cell_set[2], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[2].loc))
                                    setattr(cell_set[2], prop, False)

def hidden_quad_row(grid):
    print("17) Checking for hidden quad in row")
    for j in range(len(grid)):
        props_counts = { "prop_1" : 0, "prop_2" : 0, "prop_3" : 0, "prop_4" : 0, "prop_5" : 0, "prop_6" : 0, "prop_7" : 0, "prop_8" : 0, "prop_9" : 0}
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)):
            if grid[i][j].propcount > 4 : paired_cells.append((grid[i][j]))
            for prop in props:
                if getattr(grid[i][j], prop):
                    props_counts[prop] += 1
        prop_sets = [set for set in itertools.combinations(props, 4)]
        cell_sets = [set for set in itertools.combinations(paired_cells, 4)]
        if len(paired_cells) >= 4:
            for prop_set in prop_sets: 
                if (props_counts[prop_set[0]] >= 2 and props_counts[prop_set[0]] <= 4) and \
                   (props_counts[prop_set[1]] >= 2 and props_counts[prop_set[1]] <= 4) and \
                   (props_counts[prop_set[2]] >= 2 and props_counts[prop_set[2]] <= 4) and \
                   (props_counts[prop_set[3]] >= 2 and props_counts[prop_set[3]] <= 4)    : 
                    for cell_set in cell_sets:
                        if set(prop_set).issubset(set(cell_set[0].proplist)) and \
                        set(prop_set).issubset(set(cell_set[1].proplist)) and \
                        set(prop_set).issubset(set(cell_set[2].proplist)) and \
                        set(prop_set).issubset(set(cell_set[3].proplist)) and \
                        any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0]), getattr(cell_set[3], prop_set[0])]) and \
                        any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1]), getattr(cell_set[3], prop_set[1])]) and \
                        any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2]), getattr(cell_set[3], prop_set[2])]) and \
                        any([getattr(cell_set[0], prop_set[3]), getattr(cell_set[1], prop_set[3]), getattr(cell_set[2], prop_set[3]), getattr(cell_set[3], prop_set[3])]):
                            print('    Prop set ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ', ' + str(prop_set[2]) + ' and ' + str(prop_set[3]) + ' is a hidden pair in cell:\n    ' + str(cell_set[0]) + ' and cell:\n    ' + str(cell_set[1]) + ' in row ' + str(j)) 
                            for prop in props:
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[0], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[0].loc))
                                    setattr(cell_set[0], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[1], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[1].loc))
                                    setattr(cell_set[1], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[2], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[2].loc))
                                    setattr(cell_set[2], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[3], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[3].loc))
                                    setattr(cell_set[3], prop, False)


def hidden_quad_column(grid):
    print("18) Checking for hidden quad in column")
    for i in range(len(grid)):
        props_counts = { "prop_1" : 0, "prop_2" : 0, "prop_3" : 0, "prop_4" : 0, "prop_5" : 0, "prop_6" : 0, "prop_7" : 0, "prop_8" : 0, "prop_9" : 0}
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for j in range(len(grid)):
            if grid[i][j].propcount > 4 : paired_cells.append((grid[i][j]))
            for prop in props:
                if getattr(grid[i][j], prop):
                    props_counts[prop] += 1
        prop_sets = [set for set in itertools.combinations(props, 4)]
        cell_sets = [set for set in itertools.combinations(paired_cells, 4)]
        if len(paired_cells) >= 4:
            for prop_set in prop_sets: 
                if (props_counts[prop_set[0]] >= 2 and props_counts[prop_set[0]] <= 4) and \
                   (props_counts[prop_set[1]] >= 2 and props_counts[prop_set[1]] <= 4) and \
                   (props_counts[prop_set[2]] >= 2 and props_counts[prop_set[2]] <= 4) and \
                   (props_counts[prop_set[3]] >= 2 and props_counts[prop_set[3]] <= 4)    : 
                    for cell_set in cell_sets:
                        if set(prop_set).issubset(set(cell_set[0].proplist)) and \
                        set(prop_set).issubset(set(cell_set[1].proplist)) and \
                        set(prop_set).issubset(set(cell_set[2].proplist)) and \
                        set(prop_set).issubset(set(cell_set[3].proplist)) and \
                        any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0]), getattr(cell_set[3], prop_set[0])]) and \
                        any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1]), getattr(cell_set[3], prop_set[1])]) and \
                        any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2]), getattr(cell_set[3], prop_set[2])]) and \
                        any([getattr(cell_set[0], prop_set[3]), getattr(cell_set[1], prop_set[3]), getattr(cell_set[2], prop_set[3]), getattr(cell_set[3], prop_set[3])]):
                            print('    Prop set ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ', ' + str(prop_set[2]) + ' and ' + str(prop_set[3]) + ' is a hidden pair in cell:\n    ' + str(cell_set[0]) + ' and cell:\n    ' + str(cell_set[1]) + ' in row ' + str(j)) 
                            for prop in props:
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[0], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[0].loc))
                                    setattr(cell_set[0], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[1], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[1].loc))
                                    setattr(cell_set[1], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[2], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[2].loc))
                                    setattr(cell_set[2], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[3], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[3].loc))
                                    setattr(cell_set[3], prop, False)

def hidden_quad_group(grid):
    print("19) Checking for hidden quad in group")
    for g in groups:
        props_counts = { "prop_1" : 0, "prop_2" : 0, "prop_3" : 0, "prop_4" : 0, "prop_5" : 0, "prop_6" : 0, "prop_7" : 0, "prop_8" : 0, "prop_9" : 0}
        paired_cells = []
        prop_sets = []
        cell_sets = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j].propcount > 4  and grid[i][j].group == g: paired_cells.append((grid[i][j]))
                for prop in props:
                    if getattr(grid[i][j], prop) and grid[i][j].group == g:
                        props_counts[prop] += 1
        prop_sets = [set for set in itertools.combinations(props, 4)]
        cell_sets = [set for set in itertools.combinations(paired_cells, 4)]
        if len(paired_cells) >= 4:
            for prop_set in prop_sets: 
                if (props_counts[prop_set[0]] >= 2 and props_counts[prop_set[0]] <= 4) and \
                   (props_counts[prop_set[1]] >= 2 and props_counts[prop_set[1]] <= 4) and \
                   (props_counts[prop_set[2]] >= 2 and props_counts[prop_set[2]] <= 4) and \
                   (props_counts[prop_set[3]] >= 2 and props_counts[prop_set[3]] <= 4)    : 
                    for cell_set in cell_sets:
                        if set(prop_set).issubset(set(cell_set[0].proplist)) and \
                        set(prop_set).issubset(set(cell_set[1].proplist)) and \
                        set(prop_set).issubset(set(cell_set[2].proplist)) and \
                        set(prop_set).issubset(set(cell_set[3].proplist)) and \
                        any([getattr(cell_set[0], prop_set[0]), getattr(cell_set[1], prop_set[0]), getattr(cell_set[2], prop_set[0]), getattr(cell_set[3], prop_set[0])]) and \
                        any([getattr(cell_set[0], prop_set[1]), getattr(cell_set[1], prop_set[1]), getattr(cell_set[2], prop_set[1]), getattr(cell_set[3], prop_set[1])]) and \
                        any([getattr(cell_set[0], prop_set[2]), getattr(cell_set[1], prop_set[2]), getattr(cell_set[2], prop_set[2]), getattr(cell_set[3], prop_set[2])]) and \
                        any([getattr(cell_set[0], prop_set[3]), getattr(cell_set[1], prop_set[3]), getattr(cell_set[2], prop_set[3]), getattr(cell_set[3], prop_set[3])]):
                            print('    Prop set ' + str(prop_set[0]) + ', ' + str(prop_set[1]) + ', ' + str(prop_set[2]) + ' and ' + str(prop_set[3]) + ' is a hidden pair in cell:\n    ' + str(cell_set[0]) + ' and cell:\n    ' + str(cell_set[1]) + ' in row ' + str(j)) 
                            for prop in props:
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[0], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[0].loc))
                                    setattr(cell_set[0], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[1], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[1].loc))
                                    setattr(cell_set[1], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[2], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[2].loc))
                                    setattr(cell_set[2], prop, False)
                                if prop != prop_set[0] and prop != prop_set[1] and prop != prop_set[2] and prop != prop_set[3] and getattr(cell_set[3], prop):
                                    print('      Removing prop ' + str(prop) + ' from cell ' + str(cell_set[3].loc))
                                    setattr(cell_set[3], prop, False)

def pointing_set_row(grid):
# Removes possibilities in a row if a given group of cells requires a value
    print('20) Checking for pointing sets in rows')
    rows_by_props=[[0 for x in range(3)] for x in range(9)]
    for g in range(len(groups)):
        #Clears the array from values
        for r in range(len(rows_by_props)):
            for p in range(len(rows_by_props[r])):
                rows_by_props[r][p] = 0
        #Builds an array counting props in a given group        
        for j in range(len(grid)):
            for i in range(len(grid[j])):
                if grid[i][j].group == groups[g]:
                    for p in range(len(props)):
                        if getattr(grid[i][j], props[p]) == True: 
                            rows_by_props[p][j%3] += 1

        for prop in range(len(rows_by_props)):
            if rows_by_props[prop][0] != 0 and rows_by_props[prop][1] == 0 and rows_by_props[prop][2] == 0:
                for j in range(len(grid)):
                    for i in range(len(grid[j])):
                        if groups[g] in ['A', 'B', 'C'] and grid[i][j].group in ['A', 'B', 'C'] and grid[i][j].group != groups[g] and (j % 3) == 0 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in top row')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['D', 'E', 'F'] and grid[i][j].group in ['D', 'E', 'F'] and grid[i][j].group != groups[g] and (j % 3) == 0 and getattr(grid[i][j], props[prop]): 
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in top row')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['G', 'H', 'I'] and grid[i][j].group in ['G', 'H', 'I'] and grid[i][j].group != groups[g] and (j % 3) == 0 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in top row')
                            setattr(grid[i][j], props[prop], False)
            if rows_by_props[prop][0] == 0 and rows_by_props[prop][1] != 0 and rows_by_props[prop][2] == 0:
                for j in range(len(grid)):
                    for i in range(len(grid[j])):
                        if groups[g] in ['A', 'B', 'C'] and grid[i][j].group in ['A', 'B', 'C'] and grid[i][j].group != groups[g] and (j % 3) == 1 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in middle row')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['D', 'E', 'F'] and grid[i][j].group in ['D', 'E', 'F'] and grid[i][j].group != groups[g] and (j % 3) == 1 and getattr(grid[i][j], props[prop]): 
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in middle row')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['G', 'H', 'I'] and grid[i][j].group in ['G', 'H', 'I'] and grid[i][j].group != groups[g] and (j % 3) == 1 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in middle row')
                            setattr(grid[i][j], props[prop], False)
            if rows_by_props[prop][0] == 0 and rows_by_props[prop][1] == 0 and rows_by_props[prop][2] != 0:
                for j in range(len(grid)):
                    for i in range(len(grid[j])):
                        if groups[g] in ['A', 'B', 'C'] and grid[i][j].group in ['A', 'B', 'C'] and grid[i][j].group != groups[g] and (j % 3) == 2 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in bottom row')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['D', 'E', 'F'] and grid[i][j].group in ['D', 'E', 'F'] and grid[i][j].group != groups[g] and (j % 3) == 2 and getattr(grid[i][j], props[prop]): 
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in bottom row')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['G', 'H', 'I'] and grid[i][j].group in ['G', 'H', 'I'] and grid[i][j].group != groups[g] and (j % 3) == 2 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in bottom row')
                            setattr(grid[i][j], props[prop], False)

def pointing_set_column(grid):
# Removes possibilities in a column if a given group of cells requires a value
    print('21) Checking for pointing sets in columns')
    cols_by_props=[[0 for x in range(3)] for x in range(9)]
    for g in range(len(groups)):
        for c in range(len(cols_by_props)):
            for p in range(len(cols_by_props[c])):
                cols_by_props[c][p] = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j].group == groups[g]:
                    for p in range(len(props)):
                        if getattr(grid[i][j], props[p]) == True: 
                            cols_by_props[p][i%3] += 1

        for prop in range(len(cols_by_props)):
            if cols_by_props[prop][0] != 0 and cols_by_props[prop][1] == 0 and cols_by_props[prop][2] == 0:
                for i in range(len(grid)):
                    for j in range(len(grid[i])):
                        if groups[g] in ['A', 'D', 'G'] and grid[i][j].group in ['A', 'D', 'G'] and grid[i][j].group != groups[g] and (i % 3) == 0 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in left column')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['B', 'E', 'H'] and grid[i][j].group in ['B', 'E', 'H'] and grid[i][j].group != groups[g] and (i % 3) == 0 and getattr(grid[i][j], props[prop]): 
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in left column')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['C', 'F', 'I'] and grid[i][j].group in ['C', 'F', 'I'] and grid[i][j].group != groups[g] and (i % 3) == 0 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in left column')
                            setattr(grid[i][j], props[prop], False)
            if cols_by_props[prop][0] == 0 and cols_by_props[prop][1] != 0 and cols_by_props[prop][2] == 0:
                for i in range(len(grid)):
                    for j in range(len(grid[i])):
                        if groups[g] in ['A', 'D', 'G'] and grid[i][j].group in ['A', 'D', 'G'] and grid[i][j].group != groups[g] and (i % 3) == 1 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in middle column')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['B', 'E', 'H'] and grid[i][j].group in ['B', 'E', 'H'] and grid[i][j].group != groups[g] and (i % 3) == 1 and getattr(grid[i][j], props[prop]): 
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in middle column')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['C', 'F', 'I'] and grid[i][j].group in ['C', 'F', 'I'] and grid[i][j].group != groups[g] and (i % 3) == 1 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in middle column')
                            setattr(grid[i][j], props[prop], False)
            if cols_by_props[prop][0] == 0 and cols_by_props[prop][1] == 0 and cols_by_props[prop][2] != 0:
                for i in range(len(grid)):
                    for j in range(len(grid[i])):
                        if groups[g] in ['A', 'D', 'G'] and grid[i][j].group in ['A', 'D', 'G'] and grid[i][j].group != groups[g] and (i % 3) == 2 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in right column')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['B', 'E', 'H'] and grid[i][j].group in ['B', 'E', 'H'] and grid[i][j].group != groups[g] and (i % 3) == 2 and getattr(grid[i][j], props[prop]): 
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in right column')
                            setattr(grid[i][j], props[prop], False)
                        if groups[g] in ['C', 'F', 'I'] and grid[i][j].group in ['C', 'F', 'I'] and grid[i][j].group != groups[g] and (i % 3) == 2 and getattr(grid[i][j], props[prop]):
                            print('    Removing ' + str(props[prop]) + ' in cell ' + str(i) + '/' + str(j) + ' as group ' + str(groups[g]) + ' already has ' + str(props[prop]) + ' in right column')
                            setattr(grid[i][j], props[prop], False)

def box_line_reduction_row(grid):
    print('22) Box line reduction in rows')
    for j in range(len(grid)):
        for prop in props:
            locations = []
            for i in range(len(grid)):
                if getattr(grid[i][j], prop): locations.append(grid[i][j].group)
            if len(set(locations)) == 1: 
                print('    Prop ' + str(prop) + ' in row ' + str(j) + ' exists only in group ' + str(list(set(locations))[0]))
                for x in range(len(grid)):
                    for y in range(len(grid)):
                        if grid[x][y].group == list(set(locations))[0] and y != j and getattr(grid[x][y], prop):
                            print('      Removing ' + str(prop) + ' in cell' + str(grid[x][y].loc))
                            setattr(grid[x][y], prop, False)

def box_line_reduction_column(grid):
    print('23) Box line reduction in columns')
    for i in range(len(grid)):
        for prop in props:
            locations = []
            for j in range(len(grid)):
                if getattr(grid[i][j], prop): locations.append(grid[i][j].group)
            if len(set(locations)) == 1: 
                print('    Prop ' + str(prop) + ' in column ' + str(i) + ' exists only in group ' + str(list(set(locations))[0]))
                for x in range(len(grid)):
                    for y in range(len(grid)):
                        if grid[x][y].group == list(set(locations))[0] and x != i and getattr(grid[x][y], prop): 
                            print('      Removing ' + str(prop) + ' in cell' + str(grid[x][y].loc))
                            setattr(grid[x][y], prop, False)


def x_wing_row(grid):
    print('24) X-Wing strategy in row ')
    rows = ["row_0", "row_1", "row_2", "row_3", "row_4", "row_5", "row_6", "row_7", "row_8"]
    for prop in props:
        total_count = {"row_0": 0, "row_1": 0, "row_2": 0, "row_3": 0, "row_4": 0, "row_5": 0, "row_6": 0, "row_7": 0, "row_8": 0, }
        for j in range(len(grid)):
            for i in range(len(grid)):
                if getattr(grid[i][j], prop): 
                    if j == 0: total_count["row_0"] += 1
                    if j == 1: total_count["row_1"] += 1
                    if j == 2: total_count["row_2"] += 1
                    if j == 3: total_count["row_3"] += 1
                    if j == 4: total_count["row_4"] += 1
                    if j == 5: total_count["row_5"] += 1
                    if j == 6: total_count["row_6"] += 1
                    if j == 7: total_count["row_7"] += 1
                    if j == 8: total_count["row_8"] += 1
        for row_a in rows:
            for row_b in rows:
                if total_count[row_a] == 2 and total_count[row_b] == 2 and row_a < row_b:
                    row_a_occ = prop_row_occurences(grid, prop, rows.index(row_a))
                    row_b_occ = prop_row_occurences(grid, prop, rows.index(row_b))
                    if row_a_occ == row_b_occ:
                        print('    X-Wing for prop ' + prop + ' in row ' + str(row_a) + ' and ' + str(row_b) + ', cells ' + str(row_a_occ))
                        for a in range(len(grid)):
                            for b in range(len(grid)):
                                if (b != rows.index(row_a) and b != rows.index(row_b)) and (a == row_a_occ[0] or a == row_a_occ[1]) and getattr(grid[a][b], prop):
                                    print('      Removing ' + str(prop) + ' in cell ' + str(grid[a][b].loc))
                                    setattr(grid[a][b], prop, False)

def x_wing_column(grid):
    print('25) X-Wing strategy in column ')
    columns = ["column_0", "column_1", "column_2", "column_3", "column_4", "column_5", "column_6", "column_7", "column_8"]
    for prop in props:
        total_count = {"column_0": 0, "column_1": 0, "column_2": 0, "column_3": 0, "column_4": 0, "column_5": 0, "column_6": 0, "column_7": 0, "column_8": 0, }
        for i in range(len(grid)):
            for j in range(len(grid)):
                if getattr(grid[i][j], prop): 
                    if i == 0: total_count["column_0"] += 1
                    if i == 1: total_count["column_1"] += 1
                    if i == 2: total_count["column_2"] += 1
                    if i == 3: total_count["column_3"] += 1
                    if i == 4: total_count["column_4"] += 1
                    if i == 5: total_count["column_5"] += 1
                    if i == 6: total_count["column_6"] += 1
                    if i == 7: total_count["column_7"] += 1
                    if i == 8: total_count["column_8"] += 1
        for column_a in columns:
            for column_b in columns:
                if total_count[column_a] == 2 and total_count[column_b] == 2 and column_a < column_b:
                    column_a_occ = prop_column_occurences(grid, prop, columns.index(column_a))
                    column_b_occ = prop_column_occurences(grid, prop, columns.index(column_b))
                    if column_a_occ == column_b_occ:
                        print('    X-Wing for prop ' + prop + ' in column ' + str(column_a) + ' and ' + str(column_b) + ', cells ' + str(column_a_occ))
                        for a in range(len(grid)):
                            for b in range(len(grid)):
                                if (a != columns.index(column_a) and a != columns.index(column_b)) and (b == column_a_occ[0] or b == column_a_occ[1]) and getattr(grid[a][b], prop):
                                    print('      Removing ' + str(prop) + ' in cell ' + str(grid[a][b].loc))
                                    setattr(grid[a][b], prop, False)

def prop_row_occurences(grid, prop, row):
    occurences = []
    for i in range(len(grid)):
        if getattr(grid[i][row], prop): occurences.append(i)
    return occurences

def prop_column_occurences(grid, prop, column):
    occurences = []
    for i in range(len(grid)):
        if getattr(grid[column][i], prop): occurences.append(i)
    return occurences

def simple_colouring(grid):
    print('26) Single colouring')
    for prop in props:
        final_result = []
        count_in_cols = {"col_0": 0, "col_1": 0, "col_2": 0, "col_3": 0, "col_4": 0, "col_5": 0, "col_6": 0, "col_7": 0, "col_8": 0}
        count_in_rows = {"row_0": 0, "row_1": 0, "row_2": 0, "row_3": 0, "row_4": 0, "row_5": 0, "row_6": 0, "row_7": 0, "row_8": 0}
        count_in_grps = {"grp_A": 0, "grp_B": 0, "grp_C": 0, "grp_D": 0, "grp_E": 0, "grp_F": 0, "grp_G": 0, "grp_H": 0, "grp_I": 0}
        cls_with_prop = []
        cells_in_chain= []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if getattr(grid[i][j], prop): 
                    count_in_cols[cols[i]] += 1
                    count_in_rows[rows[j]] += 1
                    cls_with_prop.append(grid[i][j])
                for grp in grps:
                    if getattr(grid[i][j], prop) and grid[i][j].grp == grp:
                        count_in_grps[grp] += 1

        for cell_a in cls_with_prop:
            for cell_b in cls_with_prop:
                if cell_a.loc < cell_b.loc:
                    if cell_a.r == cell_b.r and count_in_rows[rows[cell_a.r]] == 2 and not (cell_a.g == cell_b.g and count_in_grps[grps[cell_a.g]] > 2):
                        # print('Cell ' + str(cell_a.loc) + ' and cell ' + str(cell_b.loc) + ' are linked in a qualifying row')
                        cells_in_chain.append((cell_a, cell_b))
                    if cell_a.c == cell_b.c and count_in_cols[cols[cell_a.c]] == 2 and not (cell_a.g == cell_b.g and count_in_grps[grps[cell_a.g]] > 2):
                        # print('Cell ' + str(cell_a.loc) + ' and cell ' + str(cell_b.loc) + ' are linked in a qualifying column')
                        cells_in_chain.append((cell_a, cell_b))
                    if cell_a.g == cell_b.g and count_in_grps[grps[cell_a.g]] == 2:
                        # print('Cell ' + str(cell_a.loc) + ' and cell ' + str(cell_b.loc) + ' are linked in a qualifying group')
                        cells_in_chain.append((cell_a, cell_b))

        cells_in_chain = list(set(cells_in_chain))

        if len(cells_in_chain) > 0:
            # print('    >> CELLS IN CHAIN: ')
            # pprint.pprint(cells_in_chain)

            chains = {}
            chain_number = 0

            while len(cells_in_chain) > 0:
                for pair in cells_in_chain:
                    temp = []
                    result = [candidate for candidate in cells_in_chain if pair[0] in candidate or pair[1] in candidate]
                    for thing in result:
                        temp.append(thing)
                        cells_in_chain.remove(thing)
                    chains[chain_number] = temp
                    chain_number += 1

            # print('    >> CHAINS:')
            # print('    Length:' + str(len(chains)))
            # pprint.pprint(chains)

            linked_chains = set()
            for key_a, value_a in chains.items():
                for key_b, value_b in chains.items():
                    if key_a < key_b:
                        for cell in value_a:
                            for tested_chain in value_b:
                                if cell[0] in tested_chain or cell[1] in tested_chain:
                                    # print('Cell ' + str(cell[0].loc) + ' or ' + str(cell[1].loc) + ' are common between ' + str(cell) + ' and ' + str(tested_chain))
                                    linked_chains.add((key_a, key_b))
            for key, value in chains.items():
                present = False
                for linked_chain in list(linked_chains):
                    if key in linked_chain:
                        present = True
                if present == False:
                    # print('Adding key ' + str(key) + ' as it is not found in:')
                    pprint.pprint(linked_chains)
                    linked_chains.add((key, key))

            # print('    >> LINKED_CHAINS')
            # pprint.pprint(linked_chains)

            merged_chains = {}
            result_number = 0

            while len(linked_chains) > 0:
                for element in list(linked_chains):
                    temp = []
                    result = [candidate for candidate in linked_chains if element[0] in candidate or element[1] in candidate]
                    for thing in result:
                        temp.append(thing)
                        linked_chains.remove(thing)
                    if len(temp) > 0:
                        merged_chains[result_number] = set(list(sum(temp,())))
                    result_number += 1
                    
            # print('MERGED CHAINS:')
            # pprint.pprint(merged_chains)

            final_result = {}
            result_number = 0

            for key, value in merged_chains.items():
                result = []
                for id in value:
                    result += chains[id]
                final_result[result_number] = result
                result_number += 1

            print('    Chains for ' + str(prop))
            pprint.pprint(final_result, indent=4)
    
            for key,chain in final_result.items():
                for pair in chain:
                    if chain.index(pair) == 0: 
                        pair[0].chainstate = "OFF"
                        pair[0].prop_states[prop] = (key, "RED")
                    if pair[0].chainstate == "OFF": 
                        pair[1].chainstate = "ON"
                        pair[1].prop_states[prop] = (key, "GRN")
                    if pair[0].chainstate == "ON": 
                        pair[1].chainstate = "OFF"
                        pair[1].prop_states[prop] = (key, "RED")

                    if pair[0].chainstate == "NONE":
                        if pair[1].chainstate == "OFF":
                            pair[0].chainstate = "ON"
                            pair[0].prop_states[prop] = (key, "GRN")
                            pair[1].chainstate = "OFF"
                            pair[1].prop_states[prop] = (key, "RED")
                        if pair[1].chainstate == "ON":
                            pair[0].chainstate = "OFF"
                            pair[0].prop_states[prop] = (key, "RED")
                            pair[1].chainstate = "ON"
                            pair[0].prop_states[prop] = (key, "GRN")
                        if pair[1].chainstate == "NONE":
                            pair[0].chainstate = "ON"
                            pair[0].prop_states[prop] = (key, "GRN")
                            pair[1].chainstate = "OFF"
                            pair[1].prop_states[prop] = (key, "RED")

        all_chains[prop] = final_result
    pprint.pprint(all_chains)

def count_props(grid): 
#Counts the total amount of props in a cell
    print('*)  Count amount of possibilities in cell')
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[i][j].propcount = 0
            for prop in range(len(props)):
                if getattr(grid[i][j], props[prop]) == True: grid[i][j].propcount += 1
            #Displays function's run outcome
            # print('Group: ' + str(grid[i][j].group) + ' X: ' + str(i + 1) + ' Y: ' + str(j + 1) + ' Count of props: ' + str(grid[i][j].propcount))
    pass

def count_total_props(grid):
    #Conts all possible marked solutions on the board
    total_props = 0
    for prop in range(len(props)):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if getattr(grid[i][j], props[prop]): total_props += 1
    return total_props

def mark_all(grid):
    print('*)  Mark all posible propositions')
# Marks all possibilties on the board
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[i][j].prop_1 = True
            grid[i][j].prop_2 = True
            grid[i][j].prop_3 = True
            grid[i][j].prop_4 = True
            grid[i][j].prop_5 = True
            grid[i][j].prop_6 = True
            grid[i][j].prop_7 = True
            grid[i][j].prop_8 = True
            grid[i][j].prop_9 = True

def mark_none(grid):
    print('*)  Clear the board')
# Marks off all possibilities on the board
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[i][j].prop_1 = False
            grid[i][j].prop_2 = False
            grid[i][j].prop_3 = False
            grid[i][j].prop_4 = False
            grid[i][j].prop_5 = False
            grid[i][j].prop_6 = False
            grid[i][j].prop_7 = False
            grid[i][j].prop_8 = False
            grid[i][j].prop_9 = False
            grid[i][j].solved = False
            grid[i][j].value = 0
    all_chains.clear()

def input_game(string, grid):
    print('*)  Input game')
    game = string
    for j in range(len(game)):
        if int(game[j]) != 0:
            print('Setting row: ' + str(int(j/9)) + ' and column: ' + str(j%9) + ' to value: ' + str(game[j]))
            grid[int(j%9)][int(j/9)].value = int(game[j])
            grid[int(j%9)][int(j/9)].solved = True

def solve_game(grid):
    overall_check(grid)
    naked_pair_row(grid)
    naked_pair_column(grid)
    naked_pair_group(grid)
    naked_triple_row(grid)
    naked_triple_column(grid)
    naked_triple_group(grid)
    naked_quad_row(grid)
    naked_quad_column(grid)
    naked_quad_group(grid)
    hidden_pair_row(grid)
    hidden_pair_column(grid)
    hidden_pair_group(grid) 
    hidden_triple_row(grid)
    hidden_triple_column(grid)
    hidden_triple_group(grid)
    hidden_quad_row(grid)
    hidden_quad_column(grid)
    hidden_quad_group(grid)
    pointing_set_row(grid)
    pointing_set_column(grid)
    box_line_reduction_row(grid)
    box_line_reduction_column(grid)
    x_wing_row(grid)
    x_wing_column(grid)
    count_props(grid)
    show_highlight(grid)
    check_singles(grid)
    check_hidden_group(grid)
    check_hidden_column(grid)
    check_hidden_row(grid) 
    draw_mesh(win)
    write_numbers(win, grid)
    display_info(win, grid)

def display_game(win, grid):
    overall_check(grid)
    show_highlight(grid)
    count_props(grid)
    draw_mesh(win)
    write_numbers(win, grid)
    display_info(win, grid)

def display_info(win, grid):
    a = 870
    b = 60
    colour_open = (150, 150, 150)
    colour_solved = (0, 0, 150)

    pygame.draw.rect(win, (0,0,0), (a, b, 270, 700))
    pygame.draw.rect(win, (25,25,25), (a, b, 270, 540))

    font = pygame.font.SysFont("comicsans", 60, bold=False)
    label_1 = font.render ('1', 1, colour_open)
    label_2 = font.render ('2', 1, colour_open)
    label_3 = font.render ('3', 1, colour_open)
    label_4 = font.render ('4', 1, colour_open)
    label_5 = font.render ('5', 1, colour_open)
    label_6 = font.render ('6', 1, colour_open)
    label_7 = font.render ('7', 1, colour_open)
    label_8 = font.render ('8', 1, colour_open)
    label_9 = font.render ('9', 1, colour_open)

    total_props = font.render(str(count_total_props(grid)), 1, colour_open)

    win.blit(label_1, (a+30, b+00))
    win.blit(label_2, (a+120, b+00))
    win.blit(label_3, (a+210, b+00))

    win.blit(label_4, (a+30, b+180))
    win.blit(label_5, (a+120, b+180))
    win.blit(label_6, (a+210, b+180))

    win.blit(label_7, (a+30, b+360))
    win.blit(label_8, (a+120, b+360))
    win.blit(label_9, (a+210, b+360))

    win.blit(total_props, (a+120, b+600))

    pygame.draw.rect(win, (50,50,50), (a+00, b+90, 90, 90))
    draw_indicator(win, grid, 1, a, b+90)
    pygame.draw.rect(win, (50,50,50), (a+90, b+90, 90, 90))
    draw_indicator(win, grid, 2, a+90, b+90)
    pygame.draw.rect(win, (50,50,50), (a+180, b+90, 90, 90))
    draw_indicator(win, grid, 3, a+180, b+90)
    pygame.draw.rect(win, (50,50,50), (a+00, b+270, 90, 90))
    draw_indicator(win, grid, 4, a, b+270)
    pygame.draw.rect(win, (50,50,50), (a+90, b+270, 90, 90))
    draw_indicator(win, grid, 5, a+90, b+270)
    pygame.draw.rect(win, (50,50,50), (a+180, b+270, 90, 90))
    draw_indicator(win, grid, 6, a+180, b+270)
    pygame.draw.rect(win, (50,50,50), (a+00, b+450, 90, 90))
    draw_indicator(win, grid, 7, a, b+450)
    pygame.draw.rect(win, (50,50,50), (a+90, b+450, 90, 90))
    draw_indicator(win, grid, 8, a+90, b+450)
    pygame.draw.rect(win, (50,50,50), (a+180, b+450, 90, 90))
    draw_indicator(win, grid, 9, a+180, b+450)

def draw_indicator(win, grid, number, x, y):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j].solved == True and grid[i][j].value == number and grid[i][j].group == 'A': 
                pygame.draw.rect(win, (150,150,150), (x, y, 30, 30))
            if grid[i][j].solved == True and grid[i][j].value == number and grid[i][j].group == 'B': 
                pygame.draw.rect(win, (150,150,150), (x+30, y, 30, 30))
            if grid[i][j].solved == True and grid[i][j].value == number and grid[i][j].group == 'C': 
                pygame.draw.rect(win, (150,150,150), (x+60, y, 30, 30))
            if grid[i][j].solved == True and grid[i][j].value == number and grid[i][j].group == 'D': 
                pygame.draw.rect(win, (150,150,150), (x, y+30, 30, 30))
            if grid[i][j].solved == True and grid[i][j].value == number and grid[i][j].group == 'E': 
                pygame.draw.rect(win, (150,150,150), (x+30, y+30, 30, 30))
            if grid[i][j].solved == True and grid[i][j].value == number and grid[i][j].group == 'F': 
                pygame.draw.rect(win, (150,150,150), (x+60, y+30, 30, 30))
            if grid[i][j].solved == True and grid[i][j].value == number and grid[i][j].group == 'G': 
                pygame.draw.rect(win, (150,150,150), (x, y+60, 30, 30))
            if grid[i][j].solved == True and grid[i][j].value == number and grid[i][j].group == 'H': 
                pygame.draw.rect(win, (150,150,150), (x+30, y+60, 30, 30))
            if grid[i][j].solved == True and grid[i][j].value == number and grid[i][j].group == 'I': 
                pygame.draw.rect(win, (150,150,150), (x+60, y+60, 30, 30))

grid = create_grid()
draw_mesh(win)
display_info(win, grid)

while not_solved:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            not_solved = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('SOLVE!')
                solve_game(grid)
            if event.key == pygame.K_a:
                mark_all(grid)
                display_game(win, grid)
            if event.key == pygame.K_s:
                mark_none(grid)
                display_game(win, grid)
            if event.key == pygame.K_d:
                display_game(win, grid)
            if event.key == pygame.K_r:
                pointing_set_row(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_c:
                pointing_set_column(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_q:
                naked_pair_row(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_w:
                naked_pair_column(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_e:
                naked_pair_group(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_i:
                hidden_pair_row(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_o:
                hidden_pair_column(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_p:
                hidden_pair_group(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_j:
                naked_triple_row(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_k:
                naked_triple_column(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_l:
                naked_triple_group(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_b:
                naked_quad_row(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_n:
                naked_quad_column(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_m:
                naked_quad_group(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_f:
                check_singles(grid)
            if event.key == pygame.K_g:
                check_hidden_group(grid)
            if event.key == pygame.K_v:
                check_hidden_column(grid)
            if event.key == pygame.K_t:
                check_hidden_row(grid)
            if event.key == pygame.K_0:
                simple_colouring(grid)
                show_highlight(grid)
                draw_mesh(win)
                write_numbers(win, grid)
            if event.key == pygame.K_1:
                input_game('800000000003600000070090200050007000000045700000100030001000068008500000090000400', grid)
                display_game(win, grid)             
            if event.key == pygame.K_2:
                input_game('000030004021006300640000002500607000360020059000903008700000093006300510400090000', grid)
                display_game(win, grid) 
            if event.key == pygame.K_3:
                input_game('309000400200709000087000000750060230600904008028050041000000590000106007006000104', grid)
                display_game(win, grid)
            if event.key == pygame.K_4:
                input_game('720096003000205000080004020000000060106503807040000000030800090000702000200430018', grid)
                display_game(win, grid)
            if event.key == pygame.K_5:
                input_game('010037000000000010600008029070049600100000003009350070390200008040000000000790060', grid)
                display_game(win, grid)
            if event.key == pygame.K_6:
                grid[0][1].prop_1 = True
                grid[0][3].prop_1 = True
                grid[1][7].prop_1 = True
                grid[2][2].prop_1 = True
                grid[2][3].prop_1 = True
                grid[2][6].prop_1 = True
                grid[3][1].prop_1 = True
                grid[3][3].prop_1 = True
                grid[4][4].prop_1 = True
                grid[4][6].prop_1 = True
                grid[5][2].prop_1 = True
                grid[5][3].prop_1 = True
                grid[6][2].prop_1 = True
                grid[6][4].prop_1 = True
                grid[7][7].prop_1 = True
                grid[8][8].prop_1 = True
                display_game(win, grid)
            if event.key == pygame.K_7:
                grid[2][3].prop_1 = True
                grid[1][4].prop_1 = True
                grid[2][5].prop_1 = True
                grid[1][6].prop_1 = True
                grid[5][3].prop_1 = True
                grid[4][5].prop_1 = True
                grid[4][7].prop_1 = True
                grid[5][7].prop_1 = True
                grid[8][4].prop_1 = True
                display_game(win, grid)

        if event.type == pygame.MOUSEBUTTONDOWN:
            ext_x = int(math.floor(event.pos[0]/block_size))
            ext_y = int(math.floor(event.pos[1]/block_size))
            int_x = int(math.floor(event.pos[0]%block_size))
            int_y = int(math.floor(event.pos[1]%block_size))
            if event.pos[0] < 810:
                if event.button == 1:
                    #will set value
                    if grid[ext_x][ext_y].solved == False:
                        grid[ext_x][ext_y].solved = True
                        if int_y < 30:
                            if int_x < 30: grid[ext_x][ext_y].value = 1
                            if int_x > 30 and int_x < 60: grid[ext_x][ext_y].value = 2
                            if int_x > 60: grid[ext_x][ext_y].value = 3
                        if int_y > 30 and int_y < 60:
                            if int_x < 30: grid[ext_x][ext_y].value = 4
                            if int_x > 30 and int_x < 60: grid[ext_x][ext_y].value = 5
                            if int_x > 60: grid[ext_x][ext_y].value = 6
                        if int_y > 60:
                            if int_x < 30: grid[ext_x][ext_y].value = 7
                            if int_x > 30 and int_x < 60: grid[ext_x][ext_y].value = 8
                            if int_x > 60: grid[ext_x][ext_y].value = 9
                    elif grid[ext_x][ext_y].solved == True:
                            grid[ext_x][ext_y].value = 0
                            grid[ext_x][ext_y].solved = False
                    if not(allow_setting_sol(grid, grid[ext_x][ext_y], ext_x, ext_y)):
                        grid[ext_x][ext_y].value = 0
                        grid[ext_x][ext_y].solved = False
                    display_game(win, grid)

                if event.button == 3:
                    #Set's a possible solution
                    allow = allow_setting_pos(grid, grid[ext_x][ext_y], ext_x, ext_y)
                    if not(allow):
                        if int_y < 30:
                            if int_x < 30: grid[ext_x][ext_y].prop_1 = not(grid[ext_x][ext_y].prop_1)
                            if int_x > 30 and int_x < 60: grid[ext_x][ext_y].prop_2 = not(grid[ext_x][ext_y].prop_2)
                            if int_x > 60: grid[ext_x][ext_y].prop_3 = not(grid[ext_x][ext_y].prop_3)
                        if int_y > 30 and int_y < 60:
                            if int_x < 30: grid[ext_x][ext_y].prop_4 = not(grid[ext_x][ext_y].prop_4)
                            if int_x > 30 and int_x < 60: grid[ext_x][ext_y].prop_5 = not(grid[ext_x][ext_y].prop_5)
                            if int_x > 60: grid[ext_x][ext_y].prop_6 = not(grid[ext_x][ext_y].prop_6)
                        if int_y > 60:
                            if int_x < 30: grid[ext_x][ext_y].prop_7 = not(grid[ext_x][ext_y].prop_7)
                            if int_x > 30 and int_x < 60: grid[ext_x][ext_y].prop_8 = not(grid[ext_x][ext_y].prop_8)
                            if int_x > 60: grid[ext_x][ext_y].prop_9 = not(grid[ext_x][ext_y].prop_9)
                        display_game(win, grid)
    pygame.display.flip()