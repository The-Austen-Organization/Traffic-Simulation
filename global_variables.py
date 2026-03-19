import pygame
import math
import random
import json
import copy
from collections import deque

ACCELERATION = 67
FRICTION = -6.7
DEBUGGER = True
F_down = False
G_down = False

RED = [255,20,20]
WHITE = [210,210,210]

pygame.init()
pygame.display.set_caption("Simulación del Tráfico")
width = 1280
height = 720
global screen
screen = pygame.display.set_mode((width, height), pygame.SCALED, vsync=1)
clock = pygame.time.Clock()

def draw_text(surface, text, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont("Fonts/PressStart2P-Regular.ttf", int(30 * camara.zoom))
    debug_surface = font.render(str(text), True, color)
    surface.blit(debug_surface, scale(pygame.Vector2(x, y)))

# We need both of these because I have to call camara.zoom because apparently using from camara import * creates a copy of zoom and not zoom itself, so it won't update.
import camara
from camara import *

from road import *

road = Roads([])
Cars = list()

from car import *