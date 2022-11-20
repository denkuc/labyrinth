from typing import Optional, Tuple, Iterator, List
import numpy as np
import sys
from math import sqrt, acos
from enum import Enum
from abc import abstractmethod, ABC


{placeholder}


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
