from typing import List

from board import Board

from cell import Cell

from constrain_solver import ConstraintSolver




class SimpleBacktrackingConstraintSolver(ConstraintSolver):
    def queueing_function(self, board: Board) -> List[Cell, int]:
        pass

    def solve_csp(self, board: Board) -> bool:
        return self.back_track({}, board)





