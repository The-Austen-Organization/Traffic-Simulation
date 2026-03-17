import pygame
import math
import random
from road import *

class Vector:
    """
    This is gonna be our own in house implementation of a vector because I don't wanna learn pygame's.
    """
    pass

ACCELERATION = 300
MAX_SPEED = 250
FRICTION = 100
TURN_SPEED = 120
SPEED = 0

pygame.init()
pygame.display.set_caption("Simulación del Tráfico")
width = 1280
height = 720
screen = pygame.display.set_mode((width, height), pygame.SCALED, vsync=1)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Fonts/PressStart2P-Regular.ttf", 30)

def draw_text(surface, text, x, y, color=(255, 255, 255)):
    debug_surface = font.render(str(text), True, color)
    surface.blit(debug_surface, (x, y))

from car import *

Cars = list()
Cars.append(Car(600, 350, 20))