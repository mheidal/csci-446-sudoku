from board import Board
from cell import Cell
from local_search_simulated_annealing_minimum_conflict_constraint_solver import \
    LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver


def main():
    board: Board = Board()
    simulated_annealing: LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver = LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver()
    solved: bool = simulated_annealing.solve_csp(board=board, _threading=True)
    pass


if __name__ == '__main__':
    main()
