import csv
import os
from enum import Enum
from typing import List

import numpy as np

# Diagram of the board:
#
#        0 1 2 3 4 5 6 7 8
#        _ _ _ _ _ _ _ _ _
#     0 |_|_|_|_|_|_|_|_|_|
#     1 |_|0|_|_|1|_|_|2|_|
#     2 |_|_|_|_|_|_|_|_|_|
#     3 |_|_|_|_|_|_|_|_|_|
#     4 |_|3|_|_|4|_|_|5|_|
#     5 |_|_|_|_|_|_|_|_|_|
#     6 |_|_|_|_|_|_|_|_|_|
#     7 |_|6|_|_|7|_|_|8|_|
#     8 |_|_|_|_|_|_|_|_|_|


from cell import Cell


class Status(Enum):
    SUCCESS = 1
    FAILURE = 2
    CONTINUE = 3


class Board:
    grid = np.zeros([9, 9], dtype=Cell)

    def __init__(self):
        self.read_in_csv()

    @property
    def value(self) -> int:
        """
        As value approaches 0 the number of violated constraints approaches 0 such that when value is 0, number of violated constraints is 0.
        :return: Number of violated constraints.
        """
        max_violated_constraints: int = pow(3, 81)  # 3^81
        violated_constraints: int = 0
        for row in self.grid:
            for cell in row:
                if cell.value in



    def read_in_csv(self) -> None:
        board_file_name: str = "Easy-P1"
        generated_grid = np.genfromtxt(f"{os.getcwd()}\\sudoku_boards\\{board_file_name}.csv", delimiter=",", dtype=int)
        row_num: int = 0
        for row in generated_grid:
            column_num: int = 0
            for cell in row:
                self.grid[row_num, column_num] = Cell([row_num, column_num], (cell if cell > 0 else 0), (True if cell > 0 else False))
                column_num = column_num + 1
            row_num = row_num + 1
        print(self.grid[0][0])


    def insert_value(self, cell: Cell, value: int) -> None:
        pass

    def hash_board(self) -> int:
        pass

    def check_success(self) -> Status:
        pass

    def get_cells_in_box(self, index: int) -> List[Cell]:
        rows = []
        cols = []
        box = []
        if int(index / 3) == 0:
            rows = [0, 1, 2]
        elif int(index / 3) == 1:
            rows = [3, 4, 5]
        elif int(index / 3) == 2:
            rows = [6, 7, 8]

        if int(index % 3) == 0:
            cols = [0, 1, 2]
        elif int(index % 3) == 1:
            cols = [3, 4, 5]
        elif int(index % 3) == 2:
            cols = [6, 7, 8]

        for row in rows:
            for col in cols:
                #TODO: I DON'T KNOW HOW TO ACCESS GRID; WHAT TYPE IS IT? Cells in the grid can be accessed in 2 ways... board[row][column] or grid[row][column]. Grid is a 2D-numpy array with size 9x9.
                box.append(self.grid[row][col])

        return box
