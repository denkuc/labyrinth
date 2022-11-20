from typing import List

from entity.cell import Cell, CellCollection
from entity.dictionaries import Direction
from game import Game
from logic.path_finder import PathFinder
from service.vector_move_definer import DirectionDefiner


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
