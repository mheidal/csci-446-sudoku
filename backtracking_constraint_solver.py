from board import *
from constrain_solver import *


class BacktrackingConstraintSolver(ConstraintSolver):

    # TODO
    def __init__(self):
        return

    def solve_csp(self, board: Board) -> bool:
        return self.recursive_backtrack(board, 0)

    def recursive_backtrack(self, board: Board, depth: int) -> bool:
        self.steps_taken += 1
        depth += 1

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

                if self.recursive_backtrack(child, depth):
                    return True

            return False

    # Method: minimum remaining values.
    # TODO: IMPLEMENT MORE, ASSESS COMPARATIVELY?
    def queueing_function(self, board: Board) -> List[Tuple[Cell, int]]:
        out = []
        for row in board.grid:
            for cell in row:
                if cell.value == 0:
                    for i in range(1, 10, 1):
                        out.append((deepcopy(cell), i))
                        # TESTING THIS - ONLY POPULATE THE QUEUE WITH ONE CELL AT A TIME?
                    return out

        # for y in temp:
        #     print(y.possible_values)
        # sorted(temp, key=lambda x: len(x.possible_values))
        # return out