import pygame
import math
import random
from car import *

pygame.init()
pygame.display.set_caption("BolaGame")
width = 1280
height = 720
screen = pygame.display.set_mode((width, height), pygame.SCALED, vsync=1)
clock = pygame.time.Clock()
# Load sprites
font = pygame.font.SysFont("Fonts/PressStart2P-Regular.ttf", 30)


RED =   [249,62,62]
GREY = [60,60,60]

ACCELERATION = 300
MAX_SPEED = 250
FRICTION = 200
TURN_SPEED = 120
SPEED = 0

def draw_text(surface, text, x, y, color=(255, 255, 255)):
    debug_surface = font.render(str(text), True, color)
    surface.blit(debug_surface, (x, y))
    
''' Spaceship code
   def update(self,delta,mouse):
      self.pos = pygame.Vector2(self.x,self.y)
      self.acc = (mouse - self.pos).normalize() * S
      self.vel[0] += self.acc[0]
      self.vel[1] += self.acc[1]
      self.x += self.vel[0]*delta + 1/2 * self.acc[0]*delta
      self.y += self.vel[1]*delta + 1/2 * self.acc[1]*delta

      
      self.velvector = pygame.Vector2(self.vel[0],self.vel[1]).normalize()


      if self.velvector.length() != 0:
         angle = self.velvector.angle_to(pygame.Vector2(1, 0))
         angle += 90
         # rotate sprite
         self.rotated_sprite = pygame.transform.rotate(self.sprite, -angle)

         # keep center consistent
         self.rect = self.rotated_sprite.get_rect(center=(self.x, self.y))
'''
  
class Road():
   pass
Cars = []
for i in range(1000):
   Cars.append(Car(2*(i+1),400,30,RED))

running = True
while running:
   screen.fill((14,154,215))
   dt = clock.tick(60) / 1000  # delta time

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False

   mouse = pygame.mouse.get_pos()

   keys = pygame.key.get_pressed()
   for car in Cars:
      car.update(dt,keys)
   background = pygame.image.load(f"TrafficSim/sprites/road.jpg").convert_alpha()
   background = pygame.transform.scale(background, (background.get_width() * 1.1, background.get_height() * 1.1))
   screen.blit(background, (width/2 - background.get_width()/2,height/2 - background.get_height()/2))
   for item in Cars:
      screen.blit(item.rotated_sprite, (item.x - item.rotated_sprite.get_width()/2,item.y - item.rotated_sprite.get_height()/2))
      #pygame.draw.rect(screen, (255, 0, 0), (item.x-item.sprite.get_width()/2, item.y-item.sprite.get_height()/2, item.sprite.get_width(), item.sprite.get_height()), 2)

   Stats_left = [
      f"ACCELERATION: {ACCELERATION}",
      f"MAX_SPEED: {MAX_SPEED}",
      f"FRICTION: {FRICTION}",
      f"TURN_SPEED: {TURN_SPEED}",
    ]
   for i in range(len(Stats_left)):
      draw_text(screen,Stats_left[i],10,100+22*i, (255, 240, 237))
   
   pygame.display.flip()

pygame.quit()
