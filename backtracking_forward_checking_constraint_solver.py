from constrain_solver import *
from board import *


class ForwardChecking(ConstraintSolver):

    def __init__(self):
        pass

    def solve_csp(self, board: Board) -> bool:
        return self.recursive_backtrack(board)

    def recursive_backtrack(self, board) -> bool:
        status = board.check_success()
        if status == Status.SUCCESS:
            super.print_output()
            return True
        elif status == Status.FAILURE:
            return False
        else:
            order = self.queueing_function(board)
            for cell, value in order:
                child = deepcopy(board)
                child.insert_value(cell, value)

        return

    def queueing_function(self, board: Board) -> List[Cell, int]:
        pass

    def remove_possible_value_row(self, board: Board, index: int, poss: int) -> None:
        row = board.grid[index]
        for cell in row:
            if poss in cell.possible_values:
                cell.possible_values.remove(poss)

        col = board.grid[index]

        for cell in col:
            if poss in cell.possible_values:
                cell.possible_values.remove(poss)

        box = board.get_cells_in_box(index)

        return

    def remove_possible_value_col(self, board: Board, index: int) -> None:
        pass

    def remove_possible_value_box(self, board: Board, index: int) -> None:
        pass
