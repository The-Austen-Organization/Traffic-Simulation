from global_variables import *

class Car():
   def __init__(self,x: float,y: float, radius: float) -> NONE:
      self.x = x
      self.y = y
      self.radius = radius
      self.angle = random.uniform(0, 2 * math.pi)
      self.vel = pygame.Vector2(math.cos(self.angle)*2,math.sin(self.angle)*2)
      self.acc = pygame.Vector2(-1,-1)
      self.end_color = color
      self.random = random.randint(1,5)
      self.sprite = pygame.image.load(f"/Users/baldwinhuang/Library/CloudStorage/ProtonDrive-huangbaldwin@proton.me-folder/Traffic-Simulation/sprites/car{self.random}.png").convert_alpha()
      self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 4, self.sprite.get_height() / 4))
      self.rect = self.sprite.get_rect(center=(self.x, self.y))
      self.pos = pygame.Vector2(self.x,self.y)
      self.acceleration = ACCELERATION
      self.max_speed = MAX_SPEED
      self.friction = FRICTION
      self.turn_speed = TURN_SPEED
      self.speed = SPEED

   def update(self, delta: float, path: list(Checkpoint)) -> NONE:
      forward = pygame.Vector2(1, 0).rotate(-self.angle)

      # --- acceleration / braking ---
      if keys[pygame.K_w]:
         self.speed += self.acceleration * delta
      if keys[pygame.K_s]:
         self.speed -= self.acceleration * delta
      if not keys[pygame.K_w] and not keys[pygame.K_s]:
         if self.speed > 0:
            self.speed -= self.friction * delta
         elif self.speed < 0:
            self.speed += self.friction * delta

      # clamp speed
      self.speed = max(-self.max_speed/2, min(self.speed, self.max_speed))
      if abs(self.speed) > 10:
         if keys[pygame.K_a]:
            self.angle += self.turn_speed * delta
         if keys[pygame.K_d]:
            self.angle -= self.turn_speed * delta

      # --- velocity follows direction ---
      self.vel = forward * self.speed
      self.pos += self.vel * delta

      self.x, self.y = self.pos
    
      # --- rotate sprite ---
      self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle-90)
      self.rect = self.rotated_sprite.get_rect(center=self.pos)
