from typing import List
from typing import Tuple


class Cell:

    # Constructor method. Assigns a location, a value, and a boolean to each cell.
    # By default, a cell has a value set to 0 and a 'preset' boolean set to False. This indicates that the cell
    # has not been assigned a value from the domain and that the cell is not one of the cells whose values are defined
    # in the initial board state.
    # Also initializes the possible_values attribute, which is a list of integers containing the domain of the cell.
    # Parameters:
    # - loc: Tuple[int, int] -- a pair of integers indicating x and y coordinates in the board's grid.
    # - val: int -- a value to be assigned to this cell. Default is 0 (unassigned).
    # - preset: bool -- indicates whether the cell is one of the variables set in the initial state. Default is False.
    # Returns:
    # - This cell object.
    def __init__(self, loc: Tuple[int, int], val: int = 0, preset: bool = False):
        self.location: Tuple[int, int] = loc
        self.value = val
        self.preset = preset
        self.possible_values: List[int] = []
        if not preset:
            self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return

    def __str__(self, default: bool = True) -> str:
        if default:
            return f"row:{self.location[0]}; column:{self.location[1]}; value:{self.value}; predetermined:{self.preset}"
        else:
            return str(self.value)

    # Utility method; sets the value of the possible_values list.
    # Parameters:
    # - poss: List[int] -- the new domain.
    # Returns: None.
    def set_possible_values(self, poss: List[int]) -> None:
        self.possible_values = poss
        return

    # Utility method; gets the index of the row containing this cell.
    # Parameters: None.
    # Returns:
    # - int: the index of the row containing this cell.
    def get_row_index(self) -> int:
        return self.location[0]

    # Utility method; gets the index of the column containing this cell.
    # Parameters: None.
    # Returns:
    # - int: the index of the column containing this cell.
    def get_col_index(self) -> int:
        return self.location[1]

    # Utility method; gets the index of the box containing this cell.
    # Parameters: None.
    # Returns:
    # - int: the index of the box containing this cell.
    def get_box_index(self) -> int:

        if int(self.location[0] / 3) == 0:
            if int(self.location[1] / 3) == 0:
                return 0
            elif int(self.location[1] / 3) == 1:
                return 1
            elif int(self.location[1] / 3) == 2:
                return 2
        elif int(self.location[0] / 3) == 1:
            if int(self.location[1] / 3) == 0:
                return 3
            elif int(self.location[1] / 3) == 1:
                return 4
            elif int(self.location[1] / 3) == 2:
                return 5
        if int(self.location[0] / 3) == 2:
            if int(self.location[1] / 3) == 0:
                return 6
            elif int(self.location[1] / 3) == 1:
                return 7
            elif int(self.location[1] / 3) == 2:
                return 8
