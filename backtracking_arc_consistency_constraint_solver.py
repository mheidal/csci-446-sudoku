
from backtracking_constraint_solver import *
from board import *

# Child class of BacktrackingConstraintSolver. This sudoku solver recursively assigns values to cells in an order
# chosen by the parent class's queuing function, checking after every insertion whether, for each cell, there exists
# some assignment of a value to that cell such that none of that cell's 'neighbors' will have no possible values left
# left for them to choose.
class ArcConsistency(BacktrackingConstraintSolver):

    def recursive_backtrack(self, board: Board, method: QueuingType) -> bool:
        self.steps_taken += 1
        status = board.check_success()
        if status == Status.SUCCESS:
            self.print_output(board)
            return True
        elif status == Status.FAILURE:
            return False
        else:
            order = self.queueing_function(board, method)
            while order != []:
                cell, value = order.pop()
                child = deepcopy(board)
                child.insert_value(cell, value)

                if not self.is_arc_consistent(child):
                    continue

                if self.recursive_backtrack(child, method):
                    return True

            return False

    # Arc consistency method. Arc consistency is a type of k-consistency; here, k = 1, so this method verifies that
    # after any given value assignment, there exists some value assignment to each unassigned variable X such that no
    # variable connected to X through k or less constraints has no possible values left to it.
    # This is accomplished by examining all arcs in the constraint satisfaction problem, which is all cell-cell pairs
    # where neither cell has been assigned a value and the two cells share a constraint.
    # These cell-cell pairs are organized as target-adjacent pairs.
    # The method tests if assigning a value to the target eliminates all values in the domain of the adjacent. If so,
    # then the helper method removes that value from the domain of the target and adds all arcs containing the target
    # back into the queue of pairs to be examined, with the target serving as the adjacent in the new pairs.
    # Parameters:
    # - board: Board -- a board state to examine for arc consistency.
    # Returns:
    # - bool -- represents whether or not the input board state is arc consistent.
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

    # Arc consistency helper method. This method takes a target cell and an adjacent cell and checks whether,
    # for each value x in the target's domain, assigning x to the target will leave the adjacent with an empty domain.
    # In the case of sudoku, assigning a value x to the target could only remove all remaining values from the
    # adjacent cell's domain if the adjacent cell's domain consists only of x.
    # If there is such a value x, x is removed from the target's domain and the method returns False.
    # If there is no such value, the method returns True.
    # Parameters:
    # - target: Cell -- One cell. The method tests if assigning any value in target's domain empties adjacent's domain.
    # - adjacent: Cell -- The other cell, connected to target by a constraint.
    # Returns:
    # - bool -- represents whether or not a value was removed from the domain of target.
    def remove_inconsistent_values(self, target: Cell, adjacent: Cell) -> bool:
        removed: Bool = False
        for x in target.possible_values:
            if adjacent.possible_values == [x]:
                target.possible_values.remove(x)
                removed = True
        return removed