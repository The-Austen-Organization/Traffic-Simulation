from global_variables import *

    
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

   background = pygame.image.load(f"/Users/baldwinhuang/Library/CloudStorage/ProtonDrive-huangbaldwin@proton.me-folder/Traffic-Simulation/sprites/road.jpg").convert_alpha()
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
