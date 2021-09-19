from typing import List

from board import Board

from cell import Cell

from constrain_solver import ConstraintSolver




class SimpleBacktrackingConstraintSolver(ConstraintSolver):

    def find_empty_cell(self, board: Board):
        for row in range(9):
            for col in range(9):
                print(board.grid[row][col].value)


    def possible_values(self):
        pass

    def queueing_function(self, board: Board) -> List[Cell, int]:
        pass

    def solve_csp(self, board: Board) -> bool:
        return self.back_track({}, board)

SimpleBacktrackingConstraintSolver().find_empty_cell()




