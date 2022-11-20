from typing import Optional, Tuple, Iterator, List
import numpy as np
import sys
from math import sqrt, acos
from enum import Enum
from abc import abstractmethod, ABC


class Collection(ABC):
    FIRST_ELEMENT_INDEX = 0
    LAST_ELEMENT_INDEX = -1

    @abstractmethod
    def __init__(self, elements):
        self.__elements = elements

    def is_empty(self) -> bool:
        return self.count() == 0

    def count(self) -> int:
        return len(self.__elements)

    def __len__(self) -> int:
        return self.count()

    def first(self):
        return (self.__elements or [None])[self.FIRST_ELEMENT_INDEX]

    def last(self):
        return (self.__elements or [None])[self.LAST_ELEMENT_INDEX]

    def get_as_tuple(self) -> tuple:
        if isinstance(self.__elements, tuple) is False:
            return tuple(self.__elements)
        else:
            return self.__elements

    def get_as_list(self) -> list:
        if isinstance(self.__elements, list) is False:
            return list(self.__elements)
        else:
            return self.__elements

    def __iter__(self):
        return iter(self.__elements)

    def __next__(self):
        element = next(self.__elements) or None
        if element is None:
            raise StopIteration

        return element

    def get_with_limit(self, limit: int) -> list:
        elements_as_list = self.get_as_list()
        if limit > len(elements_as_list):
            return elements_as_list

        return self.__elements[:limit]

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

class LocationType(Enum):
    UNKNOWN = '?'
    EMPTY = '.'
    START = 'T'
    CONTROL_ROOM = 'C'
    WALL = '#'

class Map:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

class Logger:
    @staticmethod
    def log(something):
        print(str(something), file=sys.stderr, flush=True)

class MutableCollection(Collection):
    def __init__(self, elements: Optional[list] = None):
        if elements is None:
            elements = []
        super().__init__(elements)

    def add(self, element_to_add):
        self.get_as_list().append(element_to_add)

    def extend(self, collection_to_extend):
        raise Exception('This method is not allowed for collections. Please use merge() instead!')

    def copy(self):
        return self.get_as_list().copy()

    def pop(self):
        return self.get_as_list().pop()

    def merge(self, collection: Collection):
        self.get_as_list().extend(collection.get_as_list())

    def remove(self, element_to_remove):
        self.get_as_list().remove(element_to_remove)

    def remove_all(self):
        self.get_as_list().clear()

    def _insert_at_index(self, element_to_insert, index: int):
        elements = self.get_as_list()
        elements.insert(index, element_to_insert)
        self.__init__(elements)

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

class CellBuilder:
    @staticmethod
    def build_cell(x: int, y: int) -> Cell:
        return Cell(Coordinates(x, y))

class DirectionDefiner:
    @staticmethod
    def get_direction(target_coordinates: Coordinates, player_coordinates: Coordinates) -> Direction:
        for direction, vector in VECTORS.items():
            if target_coordinates.x - player_coordinates.x == vector.x and \
                    target_coordinates.y - player_coordinates.y == vector.y:
                return direction

class Game:
    def __init__(self, game_map: Map):
        self.map: Map = game_map
        self.cells: CellCollection = CellCollection()
        self.player: Optional[Cell] = None
        self.time_is_running: bool = False

class RegionsExtractor:
    """
    Based on Sequential labeling algorithm from
    https://medium.com/@dellawen1997/connected-component-labeling-midterm-part-1-4b2aebfb277

    TODO: prettify and refactor
    """

    def __init__(self, cells: CellCollection, game_map: Map):
        self.__cells = cells
        self.__map = game_map

    def assign_regions(self):
        h = self.__map.height
        w = self.__map.width
        label = 0
        id_ = 0
        link = []

        for row in range(h):
            for col in range(w):
                cell = self.__cells.get_by_coordinates(Coordinates(col, row))
                if not cell.is_passable():
                    cell.region = 0
                else:
                    current_neighbors = self.__neighbors(col, row)
                    if current_neighbors == (0, 0):
                        label += 1
                        cell.region = label

                    else:
                        if min(current_neighbors) == 0 or current_neighbors[0] == current_neighbors[1]:
                            cell.region = max(current_neighbors)
                        else:
                            cell.region = min(current_neighbors)

                            if id_ == 0:
                                link.append(current_neighbors)
                                id_ = id_ + 1
                            else:
                                check = 0
                                for k in range(id_):
                                    # 交集
                                    tmp = set(link[k]).intersection(set(current_neighbors))
                                    if len(tmp) != 0:
                                        link[k] = set(link[k]).union(current_neighbors)
                                        np.array(link)
                                        check = check + 1

                                if check == 0:
                                    id_ = id_ + 1
                                    np.array(link)
                                    link.append(set(current_neighbors))

        for row in range(h):
            for col in range(w):
                for x in range(id_):
                    cell = self.__cells.get_by_coordinates(Coordinates(col, row))
                    if cell.region in link[x] and cell.region != 0:
                        cell.region = min(link[x])

    def __neighbors(self, i, j) -> Tuple[int, int]:
        left_cell = self.__cells.get_by_coordinates(Coordinates(i-1, j))
        above_cell = self.__cells.get_by_coordinates(Coordinates(i, j - 1))

        neighbors_tuple = (left_cell.region if left_cell else 0, above_cell.region if above_cell else 0)

        return neighbors_tuple

class PathFinder:
    """
    Based on the basic Sample algorythm from https://en.wikipedia.org/wiki/Pathfinding
    Can be improved with A* though
    """

    def __init__(self, game: Game):
        self.__game: Game = game

    def get_path(self, target: Cell) -> List[Cell]:
        explored_grid = []
        distance_to_target = 0
        target.distance_to_target = distance_to_target
        explored_grid.append(target)

        cells_to_look_around = [target]

        while True:
            distance_to_target += 1
            try:
                cells_to_look_around = self.__get_new_cells_to_look_around(
                    cells_to_look_around,
                    distance_to_target,
                    explored_grid,
                    self.__game.player
                )
            except Exception:
                break

            explored_grid += cells_to_look_around

        return self.__build_path_from_grid(explored_grid)

    def __get_new_cells_to_look_around(
            self,
            cells_to_look_around: List[Cell],
            distance_to_target: int,
            explored_grid: List[Cell],
            player: Cell
    ):
        new_cells_to_look_around = []
        for cell_to_look_around in cells_to_look_around:
            new_cells_to_look_around += self.__game.cells.get_passable_cells_around(
                cell_to_look_around.coordinates,
                explored_grid,
                new_cells_to_look_around,
                distance_to_target,
                player
            )

        return new_cells_to_look_around

    def __build_path_from_grid(self, explored_grid: List[Cell]) -> List[Cell]:
        """ removes redundant cells """
        clean_path = []

        closest = self.__game.player
        while explored_grid:
            cell_with_max_weight = explored_grid[-1]
            cells_with_max_weight = CellCollection([cell_with_max_weight])
            for cell in explored_grid:
                if cell is not cell_with_max_weight and cell.distance_to_target == cell_with_max_weight.distance_to_target:
                    cells_with_max_weight.add(cell)

            for cell in cells_with_max_weight:
                explored_grid.remove(cell)

            closest = cells_with_max_weight.get_closest(closest)
            clean_path.append(closest)

        return clean_path[::-1]

class DirectionDispatcher:
    def __init__(self, game: Game):
        self.__game: Game = game
        self.__path_finder = PathFinder(game)
        self.__path_to_start: List[Cell] = []
        self.__path_to_control: List[Cell] = []

    def get_next_direction(self) -> Direction:
        next_cell = self.__get_next_cell()

        return DirectionDefiner.get_direction(next_cell.coordinates, self.__game.player.coordinates)

    def __get_next_cell(self) -> Cell:
        # Player needs to return to the start if time is running
        if self.__game.time_is_running:
            if not self.__path_to_start:
                # save to cache, to not calculate each time
                self.__path_to_start = self.__path_finder.get_path(self.__game.cells.start)

            return self.__path_to_start.pop()

        region_cells = self.__game.cells.get_all_cells_of_region(self.__game.player.region)
        cells_border_with_unknown = self.__get_cells_near_unknown(region_cells)

        # If region is not yet fully explored
        if cells_border_with_unknown:
            closest_path = self.__find_closest_path_to_unknown(cells_border_with_unknown)

            return closest_path.pop()

        if not self.__path_to_control:
            # save to cache, to not calculate each time
            self.__path_to_control = self.__path_finder.get_path(self.__game.cells.control)

        return self.__path_to_control.pop()

    def __find_closest_path_to_unknown(self, cells_border_with_unknown):
        closest_path_length = 9999999
        closest_path = None

        # choose between several paths to avoid loops
        for cell_borders_with_unknown in cells_border_with_unknown.get_with_limit(2):
            path_to_unknown = self.__path_finder.get_path(cell_borders_with_unknown)
            if len(path_to_unknown) < closest_path_length:
                closest_path_length = len(path_to_unknown)
                closest_path = path_to_unknown

        return closest_path

    def __get_cells_near_unknown(self, region_cells: CellCollection) -> CellCollection:
        cells_near_unknown = CellCollection()
        for region_cell in region_cells:
            if self.__game.cells.is_near_unknown(region_cell.coordinates):
                cells_near_unknown.add(region_cell)

        return cells_near_unknown


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in input().split()]


# labyrinth loop
game_map = Map(c, r)
game = Game(game_map)
for i in range(r):
    for j in range(c):
        cell = CellBuilder.build_cell(j, i)
        game.cells.add(cell)

direction_dispatcher = DirectionDispatcher(game)
regions_extractor = RegionsExtractor(game.cells, game_map)

turn = 0

while True:
    turn += 1
    # kr: row where Rick is located.
    # kc: column where Rick is located.
    kr, kc = [int(i) for i in input().split()]
    current_coordinates = Coordinates(kc, kr)

    for i in range(r):
        row = input()  # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        for j, cell_type in enumerate(row):
            game.cells.update_cell(j, i, cell_type)

    regions_extractor.assign_regions()

    current_cell = game.cells.get_by_coordinates(current_coordinates)
    if current_cell.is_control():
        game.time_is_running = True

    game.player = current_cell

    selected_direction = direction_dispatcher.get_next_direction()
    print(selected_direction.value)
