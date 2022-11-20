from typing import Tuple

import numpy as np

from common.coordinates import Coordinates
from entity.cell import CellCollection
from entity.map import Map


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
