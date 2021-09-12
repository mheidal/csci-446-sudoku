import csv
import os
from enum import Enum
from typing import List

import numpy as np

from cell import Cell


class Status(Enum):
    SUCCESS = 1
    FAILURE = 2
    CONTINUE = 3


class Board:
    grid = np.zeros([9, 9], dtype=Cell)

    def __init__(self):
        self.read_in_csv()

    def read_in_csv(self) -> None:
        board_file_name: str = "Easy-P1"
        generated_grid = np.genfromtxt(f"{os.getcwd()}\\sudoku_boards\\{board_file_name}.csv", delimiter=",", dtype=int)
        row_num: int = 0
        for row in generated_grid:
            column_num: int = 0
            for cell in row:
                self.grid[row_num, column_num] = Cell([row_num, column_num], (cell if cell > 0 else 0))
                column_num = column_num + 1
            row_num = row_num + 1
        print(self.grid[8][3])


    def insert_value(self, cell: Cell, value: int) -> None:
        pass

    def hash_board(self) -> int:
        pass

    def check_success(self) -> Status:
        pass


