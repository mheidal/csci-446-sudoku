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
    domain: List[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    # def __init__(self):
    #     self.read_in_csv()

    def __init__(self):
        self.grid = np.zeros([9, 9], dtype=Cell)
        self.domain: List[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.read_in_csv()

    def __getitem__(self, row):
        """
        Allows Board to be subscriptable.
        Ex:
        test_board: Board = Board()
        cell: Cell = test_board[3][8] # where 3 is the the row and 8 is the column (indexes)

        :param row: first value passed in by the subscript.
        :return: If single subscript the row specified by the param row. If double subscript the Cell at the location row, col where col is the second subscript.
        """
        return self.grid[row]

    def row(self, cell: Cell) -> List[Cell]:
        """
        Gets the column in self.grid containing the Cell cell
        :param cell: A Cell in the row to return
        :return: A row in self.grid that contains the Cell cell
        """
        return self.grid[cell.location[0]]

    def column(self, cell: Cell) -> List[Cell]:
        """
        Gets the column in self.grid containing the Cell cell
        :param cell: A Cell in the column to return
        :return: A column in self.grid that contains the Cell cell
        """
        return self.grid[:, cell.location[1]]

    def block(self, cell: Cell) -> List[Cell]:
        """
        Gets the block in self.grid containing the Cell cell
        :param cell: A Cell in the block to return
        :return: A block in self.grid that contains the Cell cell
        """
        return {}
        #return self.get_cells_in_box(cell.location[0]) #TODO: fix when method complete.

    @property
    def value(self) -> int:
        """
        As value approaches 0 the number of violated constraints approaches 0 such that when value is 0, number of violated constraints is 0.
        :return: Number of violated constraints.
        """
        max_violated_constraints: int = pow(4, 81)  # 4^81
        violated_constraints: int = 0
        for row in self.grid:
            for cell in row:
                for other_cell in self.row(cell):
                    if other_cell != cell and cell.value == other_cell.value:
                        violated_constraints = violated_constraints + 1
                for other_cell in self.column(cell):
                    if other_cell != cell and cell.value == other_cell.value:
                        violated_constraints = violated_constraints + 1
                for other_cell in self.block(cell):
                    if other_cell != cell and cell.value == other_cell.value:
                        violated_constraints = violated_constraints + 1
                if cell.value not in Board.domain:
                    violated_constraints = violated_constraints + 1
                pass
        return violated_constraints

    def read_in_csv(self) -> None:
        board_file_name: str = "Easy-P1"
        generated_grid = np.genfromtxt(f"{os.getcwd()}/sudoku_boards/{board_file_name}.csv", delimiter=",", dtype=int)
        row_num: int = 0
        for row in generated_grid:
            column_num: int = 0
            for cell in row:
                self.grid[row_num, column_num] = Cell([row_num, column_num], (cell if cell > 0 else 0),
                                                      (True if cell > 0 else False))
                column_num = column_num + 1
            row_num = row_num + 1

git
# NOAHS PRINT FUCNTION
    def __str__(self) -> np.array:
        print_grid = np.zeros([9, 9])
        for i in range(9):
            for j in range(9):
                print_grid[i][j] = self.grid[i][j].value
        return(print_grid)


    def insert_value(self, cell: Cell, value: int) -> None:
        pass

    def hash_board(self) -> int:
        pass

    def check_success(self) -> Status:
        pass

    def get_cells_in_box(self, index: int) -> List[Cell]: # TODO @Mike why dont you just take in a row and column and return the block based on that rather than index?
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
                # TODO: I DON'T KNOW HOW TO ACCESS GRID; WHAT TYPE IS IT? Cells in the grid can be accessed in 2 ways... board[row][column] or grid[row][column]. Grid is a 2D-numpy array with size 9x9.
                box.append(self.grid[row][col])

        return box
