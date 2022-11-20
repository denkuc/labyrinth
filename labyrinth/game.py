from typing import Optional

from entity.cell import Cell, CellCollection
from entity.map import Map


class Game:
    def __init__(self, game_map: Map):
        self.map: Map = game_map
        self.cells: CellCollection = CellCollection()
        self.player: Optional[Cell] = None
        self.time_is_running: bool = False
