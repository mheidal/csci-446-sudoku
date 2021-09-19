import board
from backtracking_constraint_solver import *
from board import *


class ForwardChecking(ConstraintSolver):

    #TODO
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

                self.remove_possible_values(child, cell, value)

                for row in child.grid:
                    for entry in row:
                        if entry.possible_values.isEmpty():
                            return False

                if self.recursive_backtrack(child):
                    return True
            return False

    #Method: minimum remaining values.
    #TODO: IMPLEMENT MORE, ASSESS COMPARATIVELY?
    def queueing_function(self, board: Board) -> List[Tuple[Cell, int]]:
        temp = []
        for row in board.grid:
            for cell in row:
                temp.append(deepcopy(cell))
        sorted(temp, key=lambda x: len(x.possible_values), reversed = False)

        out = []
        for cell in temp:
            for val in cell.possible_values:
                out.append((cell, val))
        return out

    def remove_possible_values(self, board: Board, updated_cell: Cell, value: int) -> None:
        row = board.grid[updated_cell.get_row_index(), :]
        for cell in row:
            if value in cell.possible_values:
                cell.possible_values.remove(value)

        col = board.grid[:, updated_cell.get_col_index()]

        for cell in col:
            if value in cell.possible_values:
                cell.possible_values.remove(value)

        box = board.get_cells_in_box(updated_cell.get_box_index())

        for cell in box:
            if value in cell.possible_values:
                cell.possible_values.remove(value)
        return