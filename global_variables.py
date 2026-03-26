import pygame
import math
import random
import json
import copy
from collections import deque

ACCELERATION = 20
FRICTION = -10
DEBUGGER = True
DEBUGX = 30
DEBUGY = 500
INFOX = 30
INFOY = 100
F_down = False
G_down = False
M_down = True
Pause = False
DOT_SIZE = 3
ZOOM = 0.3
CARS = list()
PENDING_CARS = list() 
MIN_SPAWN_DISTANCE = 30
RAYS=1

RED = [255,20,20]
WHITE = [230,230,230]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
GREY = [37, 37, 37]

pygame.init()
pygame.display.set_caption("Simulación del Tráfico")
width = 1280
height = 720
global screen
screen = pygame.display.set_mode((width, height), pygame.SCALED, vsync=1)
clock = pygame.time.Clock()

_font_cache = {}

def draw_text(surface, text, x, y, color, font_size):
    if font_size not in _font_cache:
        _font_cache[font_size] = pygame.font.SysFont("Fonts/PressStart2P-Regular.ttf", font_size)
    font = _font_cache[font_size]
    debug_surface = font.render(str(text), True, color)
    surface.blit(debug_surface, pygame.Vector2(x, y))

# We need both of these because I have to call camara.zoom because apparently using from camara import * creates a copy of zoom and not zoom itself, so it won't update.
import camara
from camara import *

from road import *

road = Roads([])
Cars = list()

from car import *