import board
from backtracking_constraint_solver import *
from board import *


class ForwardChecking(BacktrackingConstraintSolver):

    def solve_csp(self, board: Board, method: int = 0) -> bool:
        board.initialize_possible_values()
        self.recursive_backtrack(board, 0, method)
        return self.steps_taken

    def recursive_backtrack(self, board: Board, depth: int, method: int):
        self.steps_taken += 1
        depth += 1

        print("Steps taken:", self.steps_taken)

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

                if not child.update_possible_values(cell):
                    return False

                elif self.recursive_backtrack(child, depth, method):
                    return True

            return False