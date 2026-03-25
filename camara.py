from global_variables import *

offset = pygame.Vector2(width / 2, height / 2)

zoom = 1

def scale(point: pygame.Vector2 ) -> pygame.Vector2:
    """
    The point of this function is to take in the coordenates of the actual world, and spit out the coordenates of the screen equivalent.
    """
    # Establishing the maximum range of the camara.
    global zoom
    zoom = max(zoom, 1)
    offset.x = min(offset.x, width / 2 * zoom)
    offset.x = max(offset.x, width - width / 2 * zoom)
    offset.y = min(offset.y, height / 2 * zoom)
    offset.y = max(offset.y, height - height / 2 * zoom)

    point = copy.copy(point)
    point.x -= offset.x
    point.y -= offset.y
    point.x *= zoom
    point.y *= zoom
    point.x += offset.x
    point.y += offset.y
    point.x += (offset.x - width / 2) * zoom
    point.y += (offset.y - height / 2) * zoom
    return point