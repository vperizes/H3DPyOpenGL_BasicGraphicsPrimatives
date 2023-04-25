import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Utils
from Utils import *

pygame.init()

screen_width = 1000
screen_height = 800
ortho_width = 640
ortho_height = 480

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Graphs in PyOpenGL')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, ortho_width, 0, ortho_height)  # need to flip y-scale of projection.
    # Pygame puts origin at upper left corner while openGL puts origin at lower left corner.
    # hence need to create scaling/transform method to go from one coordinate system to another


# glBegin(GL_line_strip) ends after one loop through a single line.
# This behavior allows us to keep lines separate between mouse clicks
def plot_lines():
    for line in points:  # loops to grab each line in the points array
        glBegin(GL_LINE_STRIP)
        for coords in line:
            glVertex2f(coords[0], coords[1])  # this loops lines to get individual points to draw x, y coord of mouse click
        glEnd()


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
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            line = []  # rest line array to an empty array to store new points and then append to points array
            points.append(line)
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == MOUSEMOTION and mouse_down:
            #  This is where we are using our mapping method from Utils to rescale y-coord
            p = pygame.mouse.get_pos()
            line.append((map_value(0, screen_width, 0, ortho_width, p[0]),
                        map_value(0, screen_height, ortho_height, 0, p[1])))  # we switch 0, 480 to 480, 0 b/c that's
            # what we want to map to from top to bottom

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    plot_lines()
    pygame.display.flip()
    # pygame.time.wait(100)
pygame.quit()