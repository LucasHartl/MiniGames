from enum import Enum


# an enumeration for the four directions
class Directions(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


# an enumeration for the representing modes
class Representation(Enum):
    EMPTY = 0
    SNAKE = 1
    HEAD_SNAKE = 2
    FOOD = 3
