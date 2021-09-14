
from constrain_solver import *

class BacktrackingArcConsistency(ConstraintSolver):

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

                if not self.is_arc_consistent(child):
                    return False

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

    def is_arc_consistent(self, board: Board, target: Cell) -> Bool:
        queue: List = []
        for row in board.grid:
            for entry in row:
                if cell.value == 0 and ((entry.location[0] == target.location[0])
                                        or (entry.location[1] == target.location[1])
                                        or (entry.get_box_index() == target.get_box_index())):
                    queue.append(deepcopy(target), entry)
        while queue != []:
            x1, x2 = queue.pop(0)
            if self.remove_inconsistent_values(x1, x2):
                if len(x1.possible_values == 0):
                    return False
        return True


    def remove_inconsistent_values(self, target: Cell, adjacent: Cell) -> Bool:
        removed: Bool = False
        valid_adj_assignment_exists: Bool = True
        for x in target.possible_values:
            if adjacent.possible_values == [x]:
                valid_adj_assignment_exists = False
            if not valid_adj_assignment_exists:
                target.possible_values.remove(x)
                removed = True
        return removed