from common.coordinates import Coordinates
from entity.dictionaries import VECTORS, Direction


class DirectionDefiner:
    @staticmethod
    def get_direction(target_coordinates: Coordinates, player_coordinates: Coordinates) -> Direction:
        for direction, vector in VECTORS.items():
            if target_coordinates.x - player_coordinates.x == vector.x and \
                    target_coordinates.y - player_coordinates.y == vector.y:
                return direction
