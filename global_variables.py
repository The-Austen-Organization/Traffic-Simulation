import pygame
import math
import random
import json
import copy
from collections import deque
from camara import *

ACCELERATION = 67
FRICTION = -6.7
DEBUGGER = True
F_down = False
G_down = False

RAYS=1

RED = [255,20,20]
WHITE = [210,210,210]

pygame.init()
pygame.display.set_caption("Simulación del Tráfico")
width = 1280
height = 720
global screen
screen = pygame.display.set_mode((width, height), pygame.SCALED, vsync=1)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Fonts/PressStart2P-Regular.ttf", 30)

def draw_text(surface, text, x, y, color=(255, 255, 255)):
    debug_surface = font.render(str(text), True, color)
    surface.blit(debug_surface, (x, y))

from road import *

road = Roads([])
Cars = list()

from car import *


