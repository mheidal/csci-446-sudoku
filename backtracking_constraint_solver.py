from board import *
from constrain_solver import *


class BacktrackingConstraintSolver(ConstraintSolver):

    # TODO
    def __init__(self):
        pass

    def solve_csp(self, board: Board) -> bool:
        return self.recursive_backtrack(board)

    def recursive_backtrack(self, board) -> bool:
        status = board.check_success()
        if status == Status.SUCCESS:
            self.print_output()
            return True
        elif status == Status.FAILURE:
            return False
        else:
            order = self.queueing_function(board)
            for cell, value in order:
                child = deepcopy(board)
                child.insert_value(cell, value)

                if self.recursive_backtrack(child):
                    return True

            return False

    # Method: minimum remaining values.
    # TODO: IMPLEMENT MORE, ASSESS COMPARATIVELY?
    def queueing_function(self, board: Board) -> List[Cell, int]:
        temp = []
        for row in board.grid:
            for cell in row:
                temp.append(deepcopy(cell))
        sorted(temp, key=lambda x: len(x.possible_values), reversed=False)

        out = []
        for cell in temp:
            for val in cell.possible_values:
                out.append((cell, val))
        return out
