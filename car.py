from global_variables import *
from road import *

def normalizeAngle(angle):
        angle = angle % 360
        if angle < 0:
            angle += 360
        return angle

class Car():
    def __init__(self,x: float,y: float, path_list: deque,road:Roads ) -> None:
        # X and Y are constant, they are the starting position.
        self.X = x
        self.Y = y 
        self.angle = random.uniform(0, 2 * math.pi)
        self.random = random.randint(1,5)
        self.sprite = pygame.image.load(f"sprites/car{self.random}.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 4*ZOOM, self.sprite.get_height() / 4*ZOOM))
        self.rect = self.sprite.get_rect(center=(self.X, self.Y))
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        self.pos = pygame.Vector2(self.X, self.Y)
        self.acceleration = pygame.Vector2()
        self.velocity = pygame.Vector2()
        self.path_list = path_list
        self.road = road
        self.pathOG = road.create_path(path_list)
        self.path = self.pathOG.copy()
        self.random = random.randint(1,5)
        self.sprite = pygame.image.load(f"sprites/car{self.random}.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 4*ZOOM, self.sprite.get_height() / 4*ZOOM))
        self.rect = self.sprite.get_rect(center=(self.X, self.Y))
        self.raycast = Car.RayCast(self.pos.copy(), pygame.Vector2(0, 0))
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)

    def update(self, delta: float) -> None:

        if len(self.path) == 0:
            # The point of this code is that when the car reaches the end of its path, it just resets back to the start.
            self.path = self.pathOG.copy()
            self.pos = pygame.Vector2(self.X, self.Y)
            self.velocity = pygame.Vector2(0, 0)
            self.acceleration = pygame.Vector2(0, 0)
            return

        current_checkpoint = self.path[0]

        if self.rect.collidepoint(current_checkpoint.x, current_checkpoint.y):
            self.rect = self.sprite.get_rect(center=(self.pos.x, self.pos.y))
            self.path.popleft()
            return

        direction = current_checkpoint.vector_from(self.pos.x, self.pos.y)

        self.acceleration = ACCELERATION * direction
        self.acceleration += self.velocity * FRICTION
        
        self.velocity += self.acceleration * delta

        self.pos += self.velocity

        self.angle = self.velocity.angle_to(pygame.Vector2(1, 0))

        self.raycast = Car.RayCast(self.pos.copy(), self.velocity.copy()) 

        self.ray = Checkpoint(0, 0).draw_line(self.pos, self.pos + pygame.Vector2(100, 0))

        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle-90)
        self.rect = self.rotated_sprite.get_rect(center=(self.pos.x, self.pos.y))

    class RayCast(): # one line straigh in front of th car
        def __init__(self, cart, velocity):
            self.cart = cart
            self.velocity = velocity 

        def cast(self):
            pass

        def render(self, screen):
            if self.velocity.length() > 0:
                direction = self.velocity.normalize()
                endpoint = (
                    self.cart.x + direction.x * 100,#modify the mult to change the length of the raycast
                    self.cart.y + direction.y * 100
                )
            
                pygame.draw.line(screen, (0, 255, 0),(self.cart.x, self.cart.y), endpoint)
