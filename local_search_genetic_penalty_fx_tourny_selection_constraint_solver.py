from board import Board
import numpy as np
import copy
import random
from constraint_solver import ConstraintSolver

class GA(ConstraintSolver):

    def random_board(self, board: Board):
        """ generates 1 random baord"""
        temp_board = copy.deepcopy(board)
        for row in range(9):
            for col in range(9):
                if temp_board.grid[row][col].value == 0:
                    random_number = random.randint(1, 9)
                    temp_board.grid[row][col].value = random_number
        return temp_board

    def population(self, board: Board) -> list:
        """ pop is a list to hold the population of baords"""
        pop = []
        """for loop that iterates popsize times"""
        for i in range(self.popsize):
            """temp_board is a copy of the board we are solving, so that we can manipulate the board wothout
            messing up the original board"""
            temp_board = copy.deepcopy(board)
            """ loops through the each cell in temp_board"""
            for row in range(9):
                for col in range(9):
                    """replaces all 0s with a random value between 1 and 9"""
                    if temp_board.grid[row][col].value == 0:
                        random_number = random.randint(1, 9)
                        temp_board.grid[row][col].value = random_number
            """inserts randomly generated board into pop"""
            pop.insert(i, temp_board)

        return pop

    def fitness(self, pop: list):
        """dictionary to store each board and there corresponding fitness"""
        fit_dict = {}
        """for loop that puts each baord and its corresponding fitness into fit_dict """
        for i in pop:
            fit_dict[i] = i.value
        return fit_dict

    def tournamnet_selection(self, fit_dict: dict):
        """i use pop and fit_list to retrive keys and values from fit_dict"""
        pop = list(fit_dict.keys())
        fit_list = list(fit_dict.values())
        fit_list.sort()
        """"sort fit_dict by the values"""
        sorted_fit_dict = {}
        for i in fit_list:
            for j in pop:
                if fit_dict[j] == i:
                    sorted_fit_dict[j] = fit_dict[j]
        """get keys and values from the sorted dict"""
        sorted_pop = list(sorted_fit_dict.keys())
        sorted_fit_list = list(sorted_fit_dict.values())
        """get the total fitness"""
        total_fit = sum(fit_list)
        """fit_prob_list to store all the associated probabilities with each board"""
        fit_prob_list = []
        """for loop that inserts probabilities of each board into fit_prob_list"""
        for i in range(len(fit_list)):
            """anohter way i did probability"""
            #fit_prob_list.insert(i, ((1/fit_list[i])/total_fit) * 10000)\
            fit_prob_list.insert(i, self.popsize - (i/2))
        """combatant and gladiator variables to select boards for the tournamnet"""
        combatant = random.choices(sorted_pop, weights=fit_prob_list, k=1)[0]
        gladiator = random.choices(sorted_pop, weights=fit_prob_list, k=1)[0]
        """while loop that makes sure gladiator and combatant arent the same"""
        while sorted_pop.index(combatant) == sorted_pop.index(gladiator):
            gladiator = random.choices(sorted_pop, weights=fit_prob_list, k=1)[0]
        """this is the actual tournamnet that compares the values of combatant and gladiator"""
        if gladiator.value < combatant.value:
            return gladiator
        else:
            return combatant

    """other tournamnet selction method, tried another startegy"""
    # def tournamnet_selection(self, fit_dict: dict):
    #     """i use pop and fit_list to retrive keys and values from fit_dict"""
    #     pop = list(fit_dict.keys())
    #     fit_list = list(fit_dict.values())
    #     gladiators = random.sample(pop, k=2)
    #     min = Board()
    #     for i in gladiators:
    #         if i.value < min.value:
    #             min = i
    #     return min

    def crossover(self, dad: Board, mom: Board) -> Board:
        """makes variables child_1 and child_2 that are empty boards"""
        child_1: Board = Board()
        child_2: Board = Board()
        """generates a random position in the board, this is the crossover point"""
        random_row = random.randint(0,8)
        random_col = random.randint(0,8)
        """loops through the board and crosses over the parent on each child"""
        for row in range(9):
            for col in range(9):
                if row <= random_row and col <= random_col:
                    child_1[row][col].value = mom[row][col].value
                    child_2[row][col].value = dad[row][col].value
                else:
                    child_2[row][col].value = mom[row][col].value
                    child_1[row][col].value = dad[row][col].value
        return [child_1, child_2]

    def mutate(self, children: list):
        """sets the mutation_rate, and gets the children from the children list"""
        mutation_rate = 2/81
        child_1 = children[0]
        child_2 = children[1]
        """loops through a board and muatates a cell according to the mutation rate, the muatation will be
        changing a non permanent cell  to a random value between 1 and 9, i do this for child_1 and child_2"""
        for row in range(9):
            for col in range(9):
                if random.random() < mutation_rate:
                    if not child_1[row][col].preset:
                        child_1[row][col].value = random.randint(1,9)
        for row in range(9):
            for col in range(9):
                if random.random() < mutation_rate:
                    if not child_1[row][col].preset:
                        child_2[row][col].value = random.randint(1,9)
        return [child_1, child_2]




    def replace(self, pop_val: list, fit_dict: dict):
        """this a a list of the next generation"""
        new_pop = []
        percent_of_list = 0.8
        """while loop that populates the new_pop with children from tournament selection, the percent_of_list is the
        percentage of the new_pop thats will be generaqted by the tournamnent selction"""
        while len(new_pop) < int(self.popsize * percent_of_list):
            """dad and mom are winners of a tournamnet"""
            dad = self.tournamnet_selection(fit_dict)
            mom = self.tournamnet_selection(fit_dict)
            # while (dad.value == mom.value):
            #     mom = self.tournamnet_selection(fit_dict)
            """crossovers and mutates the children and puts the in the new_pop"""
            children = self.crossover(dad, mom)
            children = self.mutate(children)
            new_pop.append(children[0])
            new_pop.append(children[1])
        """n is the number of new_pop that still needs to be popoulated"""
        n = self.popsize - len(new_pop) - 1
        """populates the rest of new_pop"""
        """inserts most fit member of the previous gen to the next gen"""
        new_pop.append(self.pop[pop_val.index(min(pop_val))])
        for i in range(n):
            """genertaes a rand_int to append a random member of the current gen to the next gen"""
            rand_int = random.randint(0, len(self.pop) - 1)
            new_pop.append(self.pop[rand_int])
            """appends memebers with highest fitnees from the current gen to the next gen"""
            # new_pop.append(self.pop[pop_val.index(min(pop_val))])
            # del pop_val[pop_val.index(min(pop_val))]
            # del self.pop[0]
            """appends new random boards to the next gen"""
            #new_pop.append(self.random_board(self.B))
        return new_pop

    def update_pop_val(self, pop: list):
        """creates a list of each boards value"""
        pop_val = []
        for i in range(len(pop)):
            pop_val.insert(i, pop[i].value)
        return pop_val

    def __init__(self):
        """creates a board, sets a popsize, creats gen variable, creates population and the the pop_vals"""
        self.used_list = []
        self.B: Board = Board(board_file_name="Hard-P3")
        self.popsize: int = 30
        gen = 0
        self.pop = self.population(self.B)
        pop_val = self.update_pop_val(self.pop)

        """while loop that runs until a boards conflicts are 0"""
        while(min(pop_val) != 0):
            min_val = min(pop_val)
            print(min_val)
            fit_dict = self.fitness(self.pop)
            self.pop = self.replace(pop_val, fit_dict)
            pop_val = self.update_pop_val(self.pop)
            """adds one to gen at the end of loop"""
            gen = gen + 1
            print("gen", gen)
        print("Total generaqtions: ", gen)
        print(self.pop[pop_val.index(0)].__str__(), gen)

    def solve_csp(self, board: Board) -> bool:
        GA()
        return True




