from global_variables import *

class Car():
    def __init__(self,x: float,y: float, path: deque([Checkpoint])) -> None:
        # X and Y are constant, they are the starting position.
        self.X = x
        self.Y = y 
        self.angle = random.uniform(0, 2 * math.pi)
        self.random = random.randint(1,5)
        self.sprite = pygame.image.load(f"sprites/car{self.random}.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 4, self.sprite.get_height() / 4))
        self.rect = self.sprite.get_rect(center=(self.X, self.Y))
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        self.pos = pygame.Vector2(self.X, self.Y)
        self.acceleration = pygame.Vector2()
        self.velocity = pygame.Vector2()
        self.pathOG = path
        self.path = self.pathOG.copy()

    def update(self, delta: float) -> None:

        if len(self.path) == 0:
            # The point of this code is that when the car reaches the end of its path, it just resets back to the start.
            self.path = self.pathOG.copy()
            self.pos = pygame.Vector2(self.X, self.Y)
            self.velocity = pygame.Vector2(0, 0)
            self.acceleration = pygame.Vector2(0, 0)
            return

        current_checkpoint = self.path[0];

        if self.rect.collidepoint(current_checkpoint.x, current_checkpoint.y):
            self.path.popleft()
            return

        direction = current_checkpoint.vector_from(self.pos.x, self.pos.y);

        self.acceleration = ACCELERATION * direction
        self.acceleration += self.velocity * FRICTION
        
        self.velocity += self.acceleration * delta

        self.pos += self.velocity

        self.angle = self.velocity.angle_to(pygame.Vector2(1, 0))

        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle-90)
        self.rect = self.rotated_sprite.get_rect(center=(self.pos.x, self.pos.y))
        
