from typing import List

from board import Board

from cell import Cell

from backtracking_constraint_solver import *


class SimpleBacktracking(BacktrackingConstraintSolver):

    def recursive_backtrack(self, board: Board):
        self.steps_taken += 1

        status = board.check_success()

        if status == Status.SUCCESS:
            self.print_output(board)
            return True
        elif status == Status.FAILURE:
            return False
        else:
            order = self.queueing_function(board)

            for cell, value in order:
                child = deepcopy(board)
                child.insert_value(cell.location, value, False)

                if self.recursive_backtrack(child):
                    return True

            return False