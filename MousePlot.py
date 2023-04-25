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
    gluOrtho2D(0, ortho_width, 0, ortho_height)  # need to flip y-scale of projection. Pygame puts origin at upper left corner while
    # openGL puts origin at lower left corner. hence need to create scaling/transform method to go from one
    # coordinate system to another


def plot_point():
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])  # this for loop loops around points array to plot x, y coord of mouse click
    glEnd()


done = False
init_ortho()
glPointSize(5)
points = []  # create an array to store the points so they do not get cleared by glClear
while not done:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            #  This is where we are using our mapping method from Utils to rescale y-coord
            p = pygame.mouse.get_pos()
            points.append((map_value(0, screen_width, 0, ortho_width, p[0]),
                           map_value(0, screen_height, ortho_height, 0, p[1])))  # we switch 0, 480 to 480, 0 b/c thats
            # what we want to map to from top to bottom

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    plot_point()
    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()
