from global_variables import *

offset = pygame.Vector2(0, 0)

zoom = 1

def scale(point: pygame.Vector2 | Checkpoint) -> pygame.Vector2:
    """
    The point of this function is to take in the coordenates of the actual world, and spit out the coordenates of the screen equivalent.
    """
    point = copy.copy(point)
    point.x -= offset.x
    point.y -= offset.y
    point.x *= zoom
    point.y *= zoom
    point.x += offset.x
    point.y += offset.y
    print(zoom)
    return point