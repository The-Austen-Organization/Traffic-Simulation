from global_variables import *
import global_variables 
from road import *

DRIVER_PROFILES = [
    # name              weight    agresivness    min_d          st_d     yld_start  yld_stop
    {"name": "Tigre++",   "w": 5,  "agr": 0.5, "min_d": 40,  "st_d": 5,  "ys": 80,  "yp": 20},
    {"name": "Tigre",     "w": 15, "agr": 1.0, "min_d": 70,  "st_d": 10, "ys": 130, "yp": 35},
    {"name": "normal",    "w": 40, "agr": 2.0, "min_d": 100, "st_d": 20, "ys": 220, "yp": 55},
    {"name": "timido",    "w": 30, "agr": 3.0, "min_d": 140, "st_d": 30, "ys": 300, "yp": 75},
    {"name": "baldwin",   "w": 10, "agr": 4.0, "min_d": 180, "st_d": 40, "ys": 370, "yp": 90},
]

def normalizeAngle(angle):
        angle = angle % 360
        if angle < 0:
            angle += 360
        return angle

def line_intersection(p1, p2, p3, p4):
    #Returns the intersection point of line p1-p2 and p3-p4, or None if they don't intersect.
    x1, y1 = p1; x2, y2 = p2
    x3, y3 = p3; x4, y4 = p4

    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if denom == 0:
        return None  

    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / denom
    u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / denom

    if 0 <= t <= 1 and 0 <= u <= 1:  # intersection both segments
        x = x1 + t*(x2-x1)
        y = y1 + t*(y2-y1)
        return (int(x), int(y))
    return None

class Car():
    def __init__(self,x: float,y: float, path_list: list, road: Roads ) -> None:
        # X and Y are constant, they are the starting position.
        self.X = x
        self.Y = y 
        self.angle = random.uniform(0, 2 * math.pi)
        self.random = random.randint(1,5)
        self.sprite = pygame.image.load(f"sprites/car{self.random}.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width(), self.sprite.get_height()))
        self.rect = self.sprite.get_rect(center=(self.X, self.Y))
        self.rect = self.rect.scale_by(1 / 16)
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        self.pos = pygame.Vector2(self.X, self.Y)
        self.acceleration = pygame.Vector2()
        self.velocity = pygame.Vector2()
        self.profile = random.choices(DRIVER_PROFILES, weights=[p["w"] for p in DRIVER_PROFILES])[0]
        self.path_list = path_list
        self.road = road
        self.pathOG = road.create_path(path_list)
        self.path = self.pathOG.copy()
        self.raycast = Car.RayCast(self, self.pos.copy(), pygame.Vector2(0, 0))

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
            self.rect = self.rect.scale_by(1 / 16)
            self.path.popleft()
            return

        direction = current_checkpoint.vector_from(self.pos.x, self.pos.y)
        brake = self.raycast.brake_power(self.profile)
        self.acceleration = ACCELERATION * direction * brake
        self.acceleration += self.velocity * FRICTION
        
        self.velocity += self.acceleration * delta

        self.pos += self.velocity 

        self.angle = self.velocity.angle_to(pygame.Vector2(1, 0))

        self.raycast = Car.RayCast(self, self.pos.copy(), self.velocity.copy())
        self.raycast.cast()

        self.ray = Checkpoint(0, 0).draw_line(self.pos, self.pos + pygame.Vector2(100, 0))

        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle-90)
        self.rect = self.rotated_sprite.get_rect(center=self.pos)
        self.rect = self.rect.scale_by(1 / 16)

    class RayCast(): # one line straight in front of the car
        def __init__(self, owner, cart, velocity, max_length=500):
            self.owner = owner        
            self.cart = cart          
            self.velocity = velocity
            self.max_length = max_length
            self.inter_point = None
            self.ray_length = max_length
            self.ray_start = pygame.Vector2(cart.x, cart.y)
            self.ray_end = pygame.Vector2(cart.x, cart.y)
            self.yld_str = 1.0

        def cast(self):
            self.inter_point = None
            self.ray_length = self.max_length * camara.zoom
            self.yld_str = 1.0

            if self.velocity.length() == 0:
                return

            direction = self.velocity.normalize()
            start = (self.cart.x, self.cart.y)
            end = (
                self.cart.x + direction.x * self.max_length,
                self.cart.y + direction.y * self.max_length
            )

            self.ray_start = start
            self.ray_end = end

            for car in Cars:  # use global Cars list directly
                if car is self.owner:
                    continue

                result = car.rect.clipline(start, end)
                if result:
                    inter_point = result[0]
                    dist = math.hypot(inter_point[0] - start[0], inter_point[1] - start[1])
                    if dist < self.ray_length:
                        self.ray_length = dist
                        self.inter_point = inter_point

            self.ray_end = (
                self.cart.x + direction.x * self.ray_length,
                self.cart.y + direction.y * self.ray_length
            )

            profile = self.owner.profile
            Ystart = profile["ys"]
            Ystop  = profile["yp"]
            Agr         = profile["agr"]

            min_yield = 1.0
            for car in Cars:
                if car is self.owner:
                    continue
                if car.raycast.velocity.length() == 0:
                    continue

                pt = line_intersection(
                    self.ray_start, self.ray_end,
                    car.raycast.ray_start, car.raycast.ray_end,
                )
                if pt is None:
                    continue

                my_dist    = math.hypot(pt[0] - start[0], pt[1] - start[1])
                other_dist = math.hypot(pt[0] - car.raycast.cart.x,
                                        pt[1] - car.raycast.cart.y)

                if my_dist <= other_dist:   # closer car has right of way
                    continue

                if my_dist <= Ystop:
                    factor = 0.0
                elif my_dist >= Ystart:
                    factor = 1.0
                else:
                    t = (my_dist - Ystop) / (Ystart - Ystop)
                    factor = t ** Agr   
                min_yield = min(min_yield, factor)

            self.yld_str = min_yield

        def render(self, screen):
            if self.velocity.length() > 0:
                direction = self.velocity.normalize()
                endpoint = pygame.Vector2(
                    self.cart.x + direction.x * self.ray_length,
                    self.cart.y + direction.y * self.ray_length
                )
                if global_variables.DEBUGGER:
                    pygame.draw.line(screen, (0, 255, 0),
                        scale(pygame.Vector2(self.cart.x, self.cart.y)), scale(endpoint))
                    if self.inter_point:
                        pygame.draw.circle(screen, (255, 0, 0), scale(pygame.Vector2(*self.inter_point)), 4)
 
                for car in Cars:
                    if car is self.owner:
                        continue
                    if car.raycast.velocity.length() == 0:
                        continue
                    pt = line_intersection(
                        self.ray_start, self.ray_end,
                        car.raycast.ray_start, car.raycast.ray_end
                    )
                    if pt and global_variables.DEBUGGER:
                        pygame.draw.circle(screen, (0, 0, 255), scale(pygame.Vector2(*pt)), 5)

        
        def brake_power(self, profile: dict) -> float:
            Agr      = profile["agr"]
            Mdt = profile["min_d"]
            Std  = profile["st_d"]

            if not self.inter_point or self.ray_length > Mdt:
                Bstr = 1.0
            elif self.ray_length <= Std:
                Bstr = 0.0
            else:
                t = (self.ray_length - Std) / (Mdt - Std)
                Bstr = t ** Agr
            return min(Bstr, self.yld_str)