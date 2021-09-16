from board import Board
from local_search_simulated_annealing_minimum_conflict_constraint_solver import LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver


def main():
    board: Board = Board()
    print(f"board.value:\t{board.value}")
    easy_p1_sol: Board = Board(board_file_name="Easy-P1-sol")
    print(f"sol.value:\t{easy_p1_sol.value}")

    simulated_annealing: LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver = LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver()
    simulated_annealing.solve_csp(board=board)
    for row in simulated_annealing.solution.grid:
        for cell in row:

    pass


if __name__ == '__main__':
    main()
