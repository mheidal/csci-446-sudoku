import csv
import os
from enum import Enum
from typing import List
from typing import Tuple

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

    def __init__(self):
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
        generated_grid = np.genfromtxt(f"{os.getcwd()}\\sudoku_boards\\{board_file_name}.csv", delimiter=",", dtype=int)
        row_num: int = 0
        for row in generated_grid:
            column_num: int = 0
            for cell in row:
                self.grid[row_num, column_num] = Cell([row_num, column_num], (cell if cell > 0 else 0),
                                                      (True if cell > 0 else False))
                column_num = column_num + 1
            row_num = row_num + 1
        self.assign_possible_values()
        return

    def insert_value(self, location: Tuple[int, int], val: int) -> None:
        x: int = location[0]
        y: int = location[1]

        target: Cell = self.grid[x][y]
        target.value = val
        target.possible_values = []

        self.assign_possible_values()
        return

    def hash_board(self) -> int:
        pass

    #TODO: THERE'S A LOT OF CODE REPETITION HERE. MAYBE IMPLEMENT A GET_CONSTRAINT_GROUPS METHOD?
    #THIS WOULD RETURN A LIST OF LISTS OF CELLS, EACH LIST OF CELLS BEING A FULL ROW COLUMN OR BOX
    def check_success(self) -> Status:
        complete_section = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for row in self.grid:
            values_in_section = []
            for cell in row:
                if cell.possible_values != []:
                    return Status.CONTINUE
                elif cell.value in values_in_section:
                    return Status.FAILURE
                else:
                    values_in_section.append(cell.value)
            if values_in_section != complete_section:
                return Status.FAILURE

        for i in range(9):
            col = self.grid[:, i]
            values_in_section = []
            for cell in col:
                if cell.possible_values != []:
                    return Status.CONTINUE
                elif cell.value in values_in_section:
                    return Status.FAILURE
                else:
                    values_in_section.append(cell.value)
            if values_in_section != complete_section:
                return Status.FAILURE

        for i in range(9):
            box = self.get_cells_in_box(i)
            values_in_section = []
            for cell in row:
                if cell.possible_values != []:
                    return Status.CONTINUE
                elif cell.value in values_in_section:
                    return Status.FAILURE
                else:
                    values_in_section.append(cell.value)
            if values_in_section != complete_section:
                return Status.FAILURE

        return Status.SUCCESS

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
                box.append(self.grid[row][col])

        return box

    #Iterates through each row, column and box, subtracting values from
    def assign_possible_values(self) -> None:

        for row in self.grid:
            reserved_values = []
            for cell in row:
                if cell.value != 0:
                    reserved_values.append(cell.value)
            for cell in row:
                for reserved_value in reserved_values:
                    if reserved_value in cell.possible_values:
                        cell.possible_values.remove(reserved_value)

        for i in range(9):
            col = self.grid[:, i]
            reserved_values = []
            for cell in col:
                if cell.value != 0:
                    reserved_values.append(cell.value)
            for cell in col:
                for reserved_value in reserved_values:
                    if reserved_value in cell.possible_values:
                        cell.possible_values.remove(reserved_value)

        for i in range(9):
            box = self.get_cells_in_box(i)
            reserved_values = []
            for cell in box:
                if cell.value != 0:
                    reserved_values.append(cell.value)
            for cell in box:
                for reserved_value in reserved_values:
                    if reserved_value in cell.possible_values:
                        cell.possible_values.remove(reserved_value)