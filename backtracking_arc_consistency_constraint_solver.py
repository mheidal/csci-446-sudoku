
from constrain_solver import *
from board import *

class ArcConsistency(ConstraintSolver):

    # TODO
    def __init__(self):
        pass

    def solve_csp(self, board: Board) -> bool:
        self.steps_taken = 0
        done = self.recursive_backtrack(board, 0)
        return done

    def recursive_backtrack(self, board, depth: int) -> bool:
        self.steps_taken += 1

        status = board.check_success()
        if status == Status.SUCCESS:
            self.print_output(board)
            return True
        elif status == Status.FAILURE:
            return False
        else:
            order = self.queueing_function(board)

            while order != []:
                cell, value = order.pop()
                child = deepcopy(board)
                child.insert_value(cell.location, value)

                if not self.is_arc_consistent(child):
                    continue

                if self.recursive_backtrack(child, depth + 1):
                    return True

            return False

    def queueing_function(self, board: Board) -> List[Tuple[Cell, int]]:
        cell_with_fewest_possible_values: Cell = None
        fewest_possible_values: float = float('inf')
        for row in board.grid:
            for cell in row:
                if len(cell.possible_values) != 0 and len(cell.possible_values) < fewest_possible_values:
                    cell_with_fewest_possible_values = cell
                    fewest_possible_values = len(cell.possible_values)
        output = []
        for value in cell_with_fewest_possible_values.possible_values:
            output.append((cell_with_fewest_possible_values, value))
        return output

    def is_arc_consistent(self, board: Board) -> bool:
        queue: List = []
        for row in board.grid:
            for cell in row:
                for other_cell in board.get_cells_with_constraint(cell):
                    if (other_cell, cell) not in queue:
                        queue.append((cell, other_cell))
        while queue != []:
            x1, x2 = queue.pop(0)
            if self.remove_inconsistent_values(x1, x2):
                if len(x1.possible_values) == 0:
                    return False
                for neighbor in board.get_cells_with_constraint(x1):
                    queue.append((neighbor, x1))
        return True

    def remove_inconsistent_values(self, target: Cell, adjacent: Cell) -> bool:
        removed: Bool = False
        for x in target.possible_values:
            if adjacent.possible_values == [x]:
                target.possible_values.remove(x)
                removed = True

        return removed
