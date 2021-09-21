from local_search_simulated_annealing_minimum_conflict_constraint_solver import \
    LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver
from simple_backtracking_constraint_solver import *
from backtracking_forward_checking_constraint_solver import *
from backtracking_arc_consistency_constraint_solver import *
from local_search_genetic_penalty_fx_tourny_selection_constraint_solver import *


def main():
    solvers = [SimpleBacktracking, ForwardChecking, ArcConsistency,
               LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver, GA]

    for solver in solvers:
        if solver is SimpleBacktracking:
            board_names: List[str] = ["Easy-P1", "Easy-P2", "Easy-P3", "Easy-P4", "Easy-P5",
                                      "Med-P1", "Med-P2", "Med-P3", "Med-P4", "Med-P5"]
        else:
            board_names: List[str] = ["Easy-P1", "Easy-P2", "Easy-P3", "Easy-P4", "Easy-P5",
                                      "Med-P1", "Med-P2", "Med-P3", "Med-P4", "Med-P5",
                                      "Hard-P1", "Hard-P2", "Hard-P3", "Hard-P4", "Hard-P5",
                                      "Evil-P1", "Evil-P2", "Evil-P3", "Evil-P4", "Evil-P5"]
        for board_name in board_names:
            print(board_name)
            csp_solver = solver()
            print(csp_solver)
            _board: Board = Board(board_file_name=board_name)
            csp_solver.solve_csp(_board)

            print()
            print('----')
            print()


if __name__ == '__main__':
    main()
