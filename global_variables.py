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

Cars = list()
Cars.append(Car(50, 440, deque([Checkpoint(900, 440), Checkpoint(1020, 300), Checkpoint(1020, 120), Checkpoint(900, 40), Checkpoint(725, 30), Checkpoint(600, 180), Checkpoint(600, 400), Checkpoint(600, 700)])))