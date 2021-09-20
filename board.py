import os
from copy import deepcopy
from enum import Enum
import platform
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

    def __init__(self, *, board_file_name: str = "Easy-P1",  grid=None):
        self.board_file_name: str = board_file_name
        if grid is None:
            self.grid = np.zeros([9, 9], dtype=Cell)
            self.read_in_csv(board_file_name)
        else:
            self.grid = deepcopy(grid)

    def __getitem__(self, row): # TODO: Broken after implementation of __str__
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
        return self.get_cells_in_box(cell.get_box_index())

    @property
    def value(self) -> int:
        """
        As value approaches 0 the number of violated constraints approaches 0 such that when value is 0, number of violated constraints is 0.
        :return: Number of violated constraints.
        """
        violated_constraints: int = 0
        for row in self.grid:
            for cell in row:
                for other_cell in self.row(cell):
                    if other_cell.get_col_index() != cell.get_col_index() and cell.value == other_cell.value:
                        violated_constraints = violated_constraints + 1
                for other_cell in self.column(cell):
                    if other_cell.get_row_index() != cell.get_row_index() and cell.value == other_cell.value:
                        violated_constraints = violated_constraints + 1
                for other_cell in self.block(cell):
                    if (not (other_cell.get_row_index() == cell.get_row_index() and other_cell.get_col_index() == cell.get_col_index())) and cell.value == other_cell.value:
                        violated_constraints = violated_constraints + 1
                if cell.value not in Board.domain:
                    violated_constraints = violated_constraints + 1
        return violated_constraints

    def cell_value(self, cell: Cell) -> int:
        """
        Number of constraints that cell violated.
        :param cell: Cell to check the number of constrains that it violates
        :return: Int representing the number of constrains that the Cell cell violates.
        """
        row: List[Cell] = self.row(cell)
        column: List[Cell] = self.column(cell)
        block: List[Cell] = self.block(cell)
        violated_constraints: int = 0
        for other_cell in row:
            if other_cell.get_col_index() != cell.get_col_index() and cell.value == other_cell.value:
                violated_constraints = violated_constraints + 1
        for other_cell in column:
            if other_cell.get_row_index() != cell.get_row_index() and cell.value == other_cell.value:
                violated_constraints = violated_constraints + 1
        for other_cell in block:
            if (not (other_cell.get_row_index() == cell.get_row_index() and other_cell.get_col_index() == cell.get_col_index())) and cell.value == other_cell.value:
                violated_constraints = violated_constraints + 1
        if cell.value not in Board.domain:
            violated_constraints = violated_constraints + 1
        return violated_constraints

    def read_in_csv(self, board_file_name: str) -> None:
        """
        Serializes a Board based on a csv representing a Sudoku board.
        :param board_file_name: Name of the csv file to serialize in the sudoku_boards directory.
        :return: None.
        """
        if platform.system() == 'Windows':
            input_file: str = f"{os.getcwd()}\\sudoku_boards\\{board_file_name}.csv"
        else:
            input_file: str = f"{os.getcwd()}/sudoku_boards/{board_file_name}.csv"
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            generated_grid = np.genfromtxt(f, dtype=int, delimiter=',')
        row_num: int = 0
        for row in generated_grid:
            column_num: int = 0
            for cell in row:
                self.grid[row_num, column_num] = Cell((row_num, column_num), (cell if cell > 0 else 0),
                                                      (True if cell > 0 else False))
                column_num = column_num + 1
            row_num = row_num + 1
        self.assign_possible_values()
        return

    def insert_value(self, cell: Cell, val: int, update_possible_values: bool = True) -> None:
        x: int = cell.location[0]
        y: int = cell.location[1]

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
                    if cell.value == neighbor.value and cell.value != 0 and cell is not neighbor:
                        return Status.FAILURE

        if cont:
            return Status.CONTINUE
        else:
            return Status.SUCCESS

    # Given a target cell, returns all cells which share a constraint with that cell.
    # i.e. all cells in the same row, column or box.
    # Note: This does return cells which have set values.
    def get_cells_with_constraint(self, target: Cell) -> List[Cell]:
        connected_cells = []
        constraints = [self.grid[target.location[0]], self.grid[:,target.location[1]], self.get_cells_in_box(target.get_box_index())]

        for constraint in constraints:
            for cell in constraint:
                if cell is not target and cell not in connected_cells:
                    connected_cells.append(cell)

        return connected_cells

    def get_box_list(self) -> List[List[Cell]]:
        """
        All of the boxes in this Board.
        :return: A List of all of the boxes in this Board.
        """
        return [self.get_cells_in_box(0), self.get_cells_in_box(1), self.get_cells_in_box(2), self.get_cells_in_box(3), self.get_cells_in_box(4), self.get_cells_in_box(5), self.get_cells_in_box(6), self.get_cells_in_box(7), self.get_cells_in_box(8)]

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

    #
    def assign_possible_values(self) -> None:

        for row in self.grid:
            for cell in row:
                neighbors = self.get_cells_with_constraint(cell)
                for neighbor in neighbors:
                    if not neighbor.value == 0:
                        if neighbor.value in cell.possible_values:
                            cell.possible_values.remove(neighbor.value)

        return
