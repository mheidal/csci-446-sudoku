from copy import deepcopy
from typing import List

from board import Board
from local_search_simulated_annealing_minimum_conflict_constraint_solver import \
    LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver


def main():
    # board_names: List[str] = ["Easy-P1", "Easy-P2", "Easy-P3", "Easy-P4", "Easy-P5",
    #                           "Med-P1", "Med-P2", "Med-P3", "Med-P4", "Med-P5",
    #                           "Hard-P1", "Hard-P2", "Hard-P3", "Hard-P4", "Hard-P5",
    #                           "Evil-P1", "Evil-P2", "Evil-P3", "Evil-P4", "Evil-P5"]
    board_names: List[str] = ["Med-P5"]
    for board_file in board_names:
        board: Board = Board(board_file_name=board_file)
        simulated_annealing: LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver = LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver()
        solved: bool = simulated_annealing.solve_csp(board=deepcopy(board), _threading=True)

    # board: Board = Board()
    # simulated_annealing: LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver = LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver()
    # solved: bool = simulated_annealing.solve_csp(board=deepcopy(board), _threading=True)


if __name__ == '__main__':
    main()


# from board import *
# from backtracking_constraint_solver import *
# from simple_backtracking_constraint_solver import *
# from backtracking_forward_checking_constraint_solver import *
# from backtracking_arc_consistency_constraint_solver import *
# from cell import *
#
# def test_constraint_solver(Constructor: ConstraintSolver):
#     board_names = []
#     if Constructor is not SimpleBacktracking:
#         board_names = ["Easy-P1","Easy-P2","Easy-P3","Easy-P4","Easy-P5",
#                       "Med-P1","Med-P2","Med-P3","Med-P4",
#                        "Hard-P1","Hard-P2","Hard-P3","Hard-P4","Hard-P5",
#                        "Evil-P1","Evil-P2","Evil-P3","Evil-P4","Evil-P5"]
#     else:
#         board_names = ["Easy-P1","Easy-P2","Easy-P3","Easy-P4","Easy-P5",
#                       "Med-P1","Med-P2","Med-P3","Med-P4"]
#
#     for board_name in board_names:
#         solver = Constructor()
#         board = Board(board_file_name = board_name)
#         print(board_name)
#         if solver.solve_csp(board):
#             print("Found solution.")
#         else:
#             print("Failed before finding solution.")
#
#         print()
#         print("--------------------------------------")
#         print()
#     return
#
#
# test_constraint_solver(ArcConsistency)
# test_constraint_solver(ForwardChecking)
# test_constraint_solver(SimpleBacktracking)