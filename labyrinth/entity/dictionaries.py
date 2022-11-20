from enum import Enum

from common.coordinates import Coordinates


class LocationType(Enum):
    UNKNOWN = '?'
    EMPTY = '.'
    START = 'T'
    CONTROL_ROOM = 'C'
    WALL = '#'


class Direction(Enum):
    UP = 'UP'
    RIGHT = 'RIGHT'
    DOWN = 'DOWN'
    LEFT = 'LEFT'


VECTORS = {
    Direction.RIGHT: Coordinates(1, 0),
    Direction.LEFT: Coordinates(-1, 0),
    Direction.UP: Coordinates(0, -1),
    Direction.DOWN: Coordinates(0, 1)
}
