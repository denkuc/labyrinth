from math import sqrt
from typing import Optional, Iterator

from common.collection import MutableCollection


class Coordinates:
    __LEFT_PIXEL = 0
    __TOP_PIXEL = 0

    def __init__(self, x: int = __LEFT_PIXEL, y: int = __TOP_PIXEL):
        self.x: int = x
        self.y: int = y

    def get_manhattan_distance(self, coordinates: 'Coordinates') -> int:
        return abs(self.x - coordinates.x) + abs(self.y - coordinates.y)

    def get_distance(self, coordinates: 'Coordinates') -> int:
        return int(self.get_distance_float(coordinates))

    def get_distance_float(self, coordinates: 'Coordinates') -> float:
        x = (pow(coordinates.x - self.x, 2))
        y = (pow(coordinates.y - self.y, 2))

        return sqrt(x + y)

    def __eq__(self, other: 'Coordinates') -> bool:
        if (self.x == other.x) and (self.y == other.y):
            return True

        return False

    def __add__(self, other: 'Coordinates') -> 'Coordinates':
        return Coordinates(self.x+other.x, self.y+other.y)

    def is_same(self, coordinates: 'Coordinates') -> bool:
        if self.x == coordinates.x and self.y == coordinates.y:
            return True

        return False

    def is_near(self, coordinates: 'Coordinates') -> bool:
        x_distance = abs(self.x - coordinates.x)
        y_distance = abs(self.y - coordinates.y)

        if (x_distance + y_distance) <= 1:
            return True

        return False

    def get_mirrored_coordinate(self, mirroring_coordinate: 'Coordinates') -> 'Coordinates':
        diff_x = mirroring_coordinate.x - self.x
        diff_y = mirroring_coordinate.y - self.y

        mirrored_x = mirroring_coordinate.x + diff_x
        mirrored_y = mirroring_coordinate.y + diff_y

        return Coordinates(mirrored_x, mirrored_y)

    def get_relative_to_coordinate(self, point: 'Coordinates') -> 'Coordinates':
        return Coordinates(self.x - point.x, self.y - point.y)

    def get_distance_to_vector_line(self, vector) -> int:
        circle_radius = self.get_distance_to_vector_line_from_zero_point(
            vector.get_relative_to_coordinate(self)
        )

        return round(circle_radius)

    @staticmethod
    def get_distance_to_vector_line_from_zero_point(vector) -> float:
        x_1 = vector.start.x
        x_2 = vector.end.x
        y_1 = vector.start.y
        y_2 = vector.end.y

        circle_radius = abs((x_2 - x_1) * y_1 + (y_1 - y_2) * x_1) / sqrt(pow(x_2 - x_1, 2) + pow(y_2 - y_1, 2))

        return circle_radius


class CoordinatesCollection(MutableCollection):
    def add(self, element_to_add: Coordinates):
        super().add(element_to_add)

    def first(self) -> Optional[Coordinates]:
        return super().first()

    def last(self) -> Optional[Coordinates]:
        return super().last()

    def __iter__(self) -> Iterator[Coordinates]:
        return super().__iter__()

    def has_coordinates(self, coordinates: Coordinates) -> bool:
        for existing_coordinates in self:
            if coordinates.is_same(existing_coordinates):
                return True

        return False

    def get_last_items(self, items_number: int) -> 'CoordinatesCollection':

        last_entities = self.get_as_list()
        if items_number < self.count():
            last_entities = last_entities[-items_number:0]

        last_items = CoordinatesCollection(last_entities)

        return last_items

    def sort_by_distance(self) -> 'CoordinatesCollection':
        ...
