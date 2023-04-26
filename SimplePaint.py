import math
import numpy as np

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Utils
from Utils import *

pygame.init()

screen_width = 1000
screen_height = 800
ortho_left = -400
ortho_right = 400
ortho_top = -400
ortho_bottom = 400

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Graphs in PyOpenGL')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)  # need to flip y-scale of projection.
    # Pygame puts origin at upper left corner while openGL puts origin at lower left corner.
    # hence need to create scaling/transform method to go from one coordinate system to another

def plot_point():
    glBegin(GL_POINTS)
    for p in points:
        glVertex2i(p[0], p[1])
    glEnd()

def plot_graph():
    glBegin(GL_LINE_STRIP)
    px: GL_DOUBLE  # px = point x
    py: GL_DOUBLE
    for px in np.arange(0, 4, 0.005):
        py = math.exp(-px) * math.cos(2* math.pi * px)
        glVertex2f(px, py)
    glEnd()

# glBegin(GL_line_strip) ends after one loop through a single line.
# This behavior allows us to keep lines separate between mouse clicks
def plot_lines():
    for line in points:  # loops to grab each line in the points array
        glBegin(GL_LINE_STRIP)
        for coords in line:
            glVertex2f(coords[0], coords[1])  # this loops lines to get individual points to draw x, y coord
            # of mouse click
        glEnd()

def save_drawing():
    file = open("drawing.txt", "w")  # open a file, use w to write into it
    file.write(str(len(points)) + "\n")  # writing the number of lines (= to length of points array)
    for l in points:
        file.write(str(len(l)) + "\n")  # writing the length of each line (# of coordinates in each line)
        for coords in l:
            file.write(str(coords[0]) + " " + str(coords[1]) + "\n")  # writing x and y points in each line
    file.close()
    print("Drawing saved")


def load_drawing():
    file = open("drawing.txt", "r")  # open a file, use r to read it
    num_of_lines = int(file.readline())  # reading out the number of lines as an integer
    global points  # declaring global allows us to write info into these arrays
    global line
    points = []
    for l in range(num_of_lines):
        line = []  # emptying line each time we read a new line
        points.append(line)
        num_of_coords = int(file.readline())
        for coord_number in range(num_of_coords):
            px, py = [float(value) for value in next(file).split()]  # read line in and splits the numbers at space
            line.append((px, py))
            print(str(px) + "," + str(py))


done = False
init_ortho()
glPointSize(5)
points = []  # storing each line array in this points array
line = []
mouse_down = False
while not done:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_drawing()
            elif event.key == pygame.K_l:
                load_drawing()
            elif event.key == pygame.K_SPACE:  # pressing space clear the screen by setting points array to empty
                points = []
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            line = []  # rest line array to an empty array to store new points and then append to points array
            points.append(line)
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == MOUSEMOTION and mouse_down:
            #  This is where we are using our mapping method from Utils to rescale y-coord
            p = pygame.mouse.get_pos()
            line.append((map_value(0, screen_width, ortho_left, ortho_right, p[0]),
                        map_value(0, screen_height, ortho_bottom, ortho_top, p[1])))  # we switch 0, 480 to 480, 0 b/c
            # that's what we want to map to from top to bottom

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    plot_lines()
    pygame.display.flip()
    # pygame.time.wait(100)
pygame.quit()