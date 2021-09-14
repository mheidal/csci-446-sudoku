
from constrain_solver import *

class BacktrackingConstraintSolver(ConstraintSolver):

    @abstractmethod
    def queueing_function(self, board: Board) -> List[Cell, int]:
        pass

