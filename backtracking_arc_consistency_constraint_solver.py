
from backtracking_constraint_solver import *
from board import *

class ArcConsistency(BacktrackingConstraintSolver):

    def recursive_backtrack(self, board) -> bool:
        self.steps_taken += 1
        if self.steps_taken % 100 == 0:
            print(self.steps_taken)
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

                if self.recursive_backtrack(child):
                    return True

            return False

    def is_arc_consistent(self, board: Board) -> bool:
        queue: List = []
        for row in board.grid:
            for cell in row:
                if cell.value == 0:
                    neighbors = board.get_cells_with_constraint(cell)
                    for neighbor in neighbors:
                        if neighbor.value == 0:
                            queue.append((cell, neighbor))

        while queue != []:
            x1, x2 = queue.pop(0)
            if self.remove_inconsistent_values(x1, x2):
                if len(x1.possible_values) == 0:
                    return False
                else:
                    neighbors = board.get_cells_with_constraint(x1)
                    for neighbor in neighbors:
                        queue.append((neighbor, x1))
        return True


    def remove_inconsistent_values(self, target: Cell, adjacent: Cell) -> bool:
        removed: Bool = False
        for x in target.possible_values:
            if adjacent.possible_values == [x]:
                target.possible_values.remove(x)
                removed = True
        return removed