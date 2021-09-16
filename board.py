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
    domain: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, board_file_name: str = "Easy-P1"):
        self.grid = np.zeros([9, 9], dtype=Cell)
        self.domain: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.read_in_csv(board_file_name)

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

    def __str__(self):
        out = ""
        for row in self.grid:
            string = ""
            for cell in row:
                if cell.location[1] % 3 == 0 and cell.location[1] > 0:
                    string += "| " + str(cell.value) + " "
                elif cell.location[0] % 3 == 0 and cell.location[1] == 0 and cell.location[0] > 0:
                    string += "------|-------|------\n"
                    string += str(cell.value) + " "
                else:
                    string += str(cell.value) + " "
            out += string + "\n"
        return out

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
        # return self.get_cells_in_box(cell.location[0]) #TODO: fix when method complete.

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

    def read_in_csv(self, board_file_name: str) -> None:
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

    def insert_value(self, location: Tuple[int, int], val: int, update_possible_values: bool = True) -> None:
        x: int = location[0]
        y: int = location[1]

        target: Cell = self.grid[x][y]
        target.value = val
        target.possible_values = []

        if update_possible_values:
            self.assign_possible_values()
        return

    def hash_board(self) -> int:
        pass

    # Checks whether the board is in a success state (all rows, columns, and boxes full and with no constraints),
    # a failure state (any constraint is violated), or a continue state (not failure and the board is incomplete)
    def check_success(self) -> Status:

        cont: bool = False

        for row in self.grid:
            for cell in row:
                if cell.value == 0:
                    cont = True
                    continue
                neighbors = self.get_cells_with_constraint(cell)
                for neighbor in neighbors:
                    if cell.value == neighbor.value and cell.value != 0:
                        return Status.FAILURE

        if cont:
            return Status.CONTINUE
        else:
            return Status.SUCCESS

    # Given a target cell, returns all cells which share a constraint with that cell.
    # i.e. all cells in the same row, column or box.
    # TODO: THIS DOESN'T WORK. PROBLEM WITH THIS METHOD? OR WITH get_cells_in_box MAYBE?
    def get_cells_with_constraint(self, target: Cell) -> List[Cell]:
        connected_cells = []
        constraints = [self.grid[target.location[0]], self.grid[:,target.location[1]], self.get_cells_in_box(target.get_box_index())]

        for constraint in constraints:
            for cell in constraint:
                if cell is not target and cell not in connected_cells:
                    connected_cells.append(cell)

        return connected_cells

    def get_cells_in_box(self, index: int) -> List[
        Cell]:  # TODO @Mike why dont you just take in a row and column and return the block based on that rather than index?
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

    # TODO: COULD BE A LOT MORE ELEGANT.
    # TODO: INTEGRATE get_cells_with_constraint
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
