from cell import *
from backtracking_constraint_solver import *
from board import *

# def remove_inconsistent_values(target: Cell, adjacent: Cell) -> bool:
#     removed: Bool = False
#     valid_adj_assignment_exists: bool = True
#     for x in target.possible_values:
#         print("investigating", x)
#         print("adj poss values is", adjacent.possible_values)
#         print(adjacent.possible_values == [x])
#         if adjacent.possible_values == [x]:
#             target.possible_values.remove(x)
#             removed = True
#
#     return removed

def test():
    b = Board()
    print(b)
    return
test()