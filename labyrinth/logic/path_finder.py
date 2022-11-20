from typing import List

from entity.cell import Cell, CellCollection
from game import Game


class PathFinder:
    """
    Based on the basic Sample algorythm from https://en.wikipedia.org/wiki/Pathfinding
    Can be improved with A* though http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
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
