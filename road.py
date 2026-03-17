from global_variables import *

class Checkpoint():
    def __init__(self, x: float, y: float) -> NONE:
        self.x = x;
        self.y = y;
    def distance_from(self, x: float, y: float) -> float:
        """
        This finds the eucledian distance between any point and this checkpoint. It takes the coordenate of the other checkpoint as an input.
        """
        return ( (self.x - x)**2 + (self.y - y)**2 )**0.5
    def vector_from(self, x: float, y: float) -> tuple:
        """
        The point of this function is to return a normalized 2D vector pointing at this check point from the perspective of the car.
        """

class Road():
    def __init__(self, points: Checkpoint) -> NONE:
        # Keep this variable private. The __ means its private.
        self.__road = points
    def __getitem__(self, index: int) -> Checkpoint:
        return __road[index]

    def __setitem__(self, index: int, value: Checkpoint) -> NONE:
        __road[index] = value
        
