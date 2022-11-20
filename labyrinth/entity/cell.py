from typing import Optional, Iterator, List

from common.collection import MutableCollection
from common.coordinates import Coordinates
from entity.dictionaries import LocationType, VECTORS


class Cell:
    def __init__(self, coordinates: Coordinates):
        self.coordinates: Coordinates = coordinates
        self.type: Optional[LocationType] = None
        self.distance_to_target: Optional[int] = 0
        self.region: int = 0

    def is_passable(self) -> bool:
        return self.is_empty() or self.is_control() or self.is_start()

    def is_wall(self) -> bool:
        return self.type == LocationType.WALL

    def is_empty(self) -> bool:
        return self.type == LocationType.EMPTY

    def is_control(self) -> bool:
        return self.type == LocationType.CONTROL_ROOM

    def is_start(self) -> bool:
        return self.type == LocationType.START

    def is_unknown(self) -> bool:
        return self.type == LocationType.UNKNOWN


class CellCollection(MutableCollection):
    def __init__(self, elements: Optional[list] = None):
        super().__init__(elements)
        self.start: Optional[Cell] = None
        self.control: Optional[Cell] = None
        self.__map = {}

    def update_cell(self, j: int, i: int, cell_type: str):
        cell = self.get_by_coordinates(Coordinates(j, i))
        cell.type = LocationType(cell_type)
        if not self.start and cell.is_start():
            self.start = cell

        if not self.control and cell.is_control():
            self.control = cell

    def add(self, element_to_add: Cell):
        self.__map.setdefault(element_to_add.coordinates.x, {})[element_to_add.coordinates.y] = element_to_add
        super().add(element_to_add)

    def get_by_coordinates(self, coordinates: Coordinates) -> Optional[Cell]:
        return self.__map.get(coordinates.x, {}).get(coordinates.y, None)

    def is_near_unknown(self, coordinates: Coordinates) -> bool:
        for vector in VECTORS.values():
            cell_around = self.get_by_coordinates(coordinates + vector)
            if cell_around and cell_around.is_unknown():
                return True

        return False

    def get_passable_cells_around(
            self,
            coordinates: Coordinates,
            explored_grid: List[Cell],
            new_cells_to_look_around: List[Cell],
            distance_to_target: int,
            player
    ):
        passable_cells_around = []
        for vector in VECTORS.values():
            cell_around = self.get_by_coordinates(coordinates + vector)
            if cell_around is player:
                raise Exception

            if not cell_around or not cell_around.is_passable():
                continue

            if cell_around in explored_grid:
                continue

            if cell_around in new_cells_to_look_around:
                continue

            cell_around.distance_to_target = distance_to_target
            passable_cells_around.append(cell_around)

        return passable_cells_around

    def get_all_cells_of_region(self, region: int) -> 'CellCollection':
        all_of_region = CellCollection()
        for cell in self:
            if cell.region == region:
                all_of_region.add(cell)

        return all_of_region

    def get_closest(self, cell_to_find: Cell) -> Cell:
        closest_distance = 999999
        closest_cell = None
        for cell in self:
            distance = cell_to_find.coordinates.get_manhattan_distance(cell.coordinates)
            if distance < closest_distance:
                closest_distance = distance
                closest_cell = cell

        return closest_cell

    def __iter__(self) -> Iterator[Cell]:
        return super().__iter__()
