from common.coordinates import Coordinates
from entity.cell import Cell


class CellBuilder:
    @staticmethod
    def build_cell(x: int, y: int) -> Cell:
        return Cell(Coordinates(x, y))
