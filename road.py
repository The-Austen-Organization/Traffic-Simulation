from global_variables import *

class Checkpoint():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    def distance_from(self, x: float, y: float) -> float:
        """
        This finds the eucledian distance between any point and this checkpoint. It takes the coordenate of the other checkpoint as an input.
        """
        return ( (self.x - x)**2 + (self.y - y)**2 )**0.5
    def vector_from(self, x: float, y: float) -> pygame.Vector2:
        """
        The point of this function is to return a normalized 2D vector pointing at this check point from the perspective of the car.
        """
        direction = pygame.Vector2()
        direction.x = self.x - x
        direction.y = self.y - y
        direction = direction.normalize()

        return direction
    def draw_dot(self):
        pygame.draw.circle(screen,RED,(self.x,self.y),30)
    def draw_line(self,pos1,pos2):
        pygame.draw.line(screen, WHITE, pos1, pos2, 1)

class Roads():
    """
    The road just includes all the checkpoints, so that we can just call Road[x] instead of writinout the entire checkpoint by scrath.
    """
    def __init__(self, points: list) -> None:
        # Keep this variable private. The __ means its private.
        self.road = points
    def __getitem__(self, index: int) -> Checkpoint:
        return self.road[index]
    def __setitem__(self, index: int, value: Checkpoint) -> None:
        self.road[index] = value
    def create_path(self, point: list) -> deque:
        """his function is going to take the inx of a bunch of the checkpoints, and it will return the deque of all those check points."""
        path = deque()
        for i in point:
            path.append(self.road[i])
        return path
