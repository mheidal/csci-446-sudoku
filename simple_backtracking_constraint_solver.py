from typing import List

from board import Board

from cell import Cell

from backtracking_constraint_solver import *


class SimpleBacktrackingConstraintSolver(BacktrackingConstraintSolver):

    def recursive_backtrack(self, board: Board, depth: int, method: int):
        self.steps_taken += 1
        depth += 1

        status = board.check_success()

        if status == Status.SUCCESS:
            self.print_output(board)
            return True
        elif status == Status.FAILURE:
            return False
        else:
            order = self.queueing_function(board, method)

            for cell, value in order:
                child = deepcopy(board)
                child.insert_value(cell.location, value, False)

                if self.recursive_backtrack(child, depth, method):
                    return True

            return False