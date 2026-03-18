import pygame
import math
import random
from collections import deque
from road import *

ACCELERATION = 67
FRICTION = -6.7

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

road = Roads([
    Checkpoint(900, 440), 
    Checkpoint(1020, 300), 
    Checkpoint(1020, 120), 
    Checkpoint(900, 40), 
    Checkpoint(725, 30), 
    Checkpoint(600, 180), 
    Checkpoint(600, 400), 
    Checkpoint(600, 800), 
    Checkpoint(-100, 440),
    Checkpoint(300, -100),
    Checkpoint(225, 800)
])

Cars = list()
Cars.append(Car(-100, 440, road.create_path([0, 1, 2, 3, 4, 5, 6, 7])))
Cars.append(Car(600, 800, road.create_path([6, 5, 4, 3, 2, 1, 0, 8])))
Cars.append(Car(300, 800, road.create_path([9])))
Cars.append(Car(225, -100, road.create_path([10])))