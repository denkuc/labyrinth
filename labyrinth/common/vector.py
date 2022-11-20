from math import sqrt, acos

from common.coordinates import Coordinates


class Vector:
    def __init__(self, start: Coordinates, end: Coordinates):
        self.start = start
        self.end = end
        self.radius_coordinate = self.end.get_relative_to_coordinate(self.start)

    @property
    def start(self) -> Coordinates:
        return self.__start

    @start.setter
    def start(self, start: Coordinates):
        self.__start = start

    @property
    def end(self) -> Coordinates:
        return self.__end

    @end.setter
    def end(self, end: Coordinates):
        self.__end = end

    @property
    def radius_coordinate(self) -> Coordinates:
        return self.__radius_coordinate

    @radius_coordinate.setter
    def radius_coordinate(self, radius_coordinate: Coordinates):
        self.__radius_coordinate = radius_coordinate

    def get_relative_to_coordinate(self, point: Coordinates) -> 'Vector':
        relative_vector = Vector(
            self.start.get_relative_to_coordinate(point),
            self.end.get_relative_to_coordinate(point),
        )

        return relative_vector

    def get_length(self) -> float:
        end_x = self.radius_coordinate.x
        end_y = self.radius_coordinate.y

        length = sqrt(pow(end_x, 2) + pow(end_y, 2))

        return length

    def get_scalar_product_with(self, other: 'Vector') -> int:
        x_1 = self.radius_coordinate.x
        y_1 = self.radius_coordinate.y
        x_2 = other.radius_coordinate.x
        y_2 = other.radius_coordinate.y

        scalar_product = x_1 * x_2 + y_1 * y_2

        return scalar_product

    def get_angle_to(self, other: 'Vector'):
        angle_cos = self.get_scalar_product_with(other) / (self.get_length() + other.get_length())
        angle = acos(angle_cos)

        if other.radius_coordinate.y < self.radius_coordinate.y:
            angle = angle * -1

        return angle
