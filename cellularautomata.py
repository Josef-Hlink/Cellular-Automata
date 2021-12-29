import typing
import numpy as np

class CellularAutomata:

    def __init__(self, rule_number: int):
        """:param rule_number: rule number in decimal notation"""
        self.rule_number: int = rule_number

    def __call__(self, c0: typing.List[int], t: int) -> typing.List[int]:
        """"
        Evaluate for T timesteps. Return Ct for a given C0.
        :param c0: init pattern
        :t: iteration that is to be returned
        """
        self.c0: typing.List[int] = c0
        self.cell_count: int = len(c0)
        self.t: int = t
        self.start()
        return self.result
        
    def start(self) -> None:
        """Sets starting conditions"""
        self.cells: typing.List[int] = [c for c in self.c0] # set cells from init pattern
        self.__next_state: typing.List[int] = [0 for _ in self.c0] # initialize next state to be all zeros
        self.result: typing.List[int] = [0 for _ in self.c0] # initialize the result to be all zeros
        self.ruleset = self.get_ruleset(self.rule_number)
        self.iteration: int = 0
        self.visualize: bool = True # can be set to False if no visualization is wanted
        self.set_colors() # changing colors can be done in the function
        self.run()

    def run(self) -> None:
        """Runs all of the iterations for the CA"""
        if self.t == None:
            return
        for iteration in range(self.t+1):
            if self.visualize:
                self.print_iteration() # print visualization
            if not iteration == self.t:
                self.update_state() # update cells
                self.iteration += 1
        # for loop ends, self.cells now is a list that represents iteration t
        self.result = self.cells.copy()
        return

    def update_state(self) -> None:
        """
        For each cell, calculate that cells next state depending on the current rule.
        Then copy the next state to the current state
        """
        for c in range(0, self.cell_count):
            left_neighbor = self.cell_count - 1 if c == 0 else c - 1
            right_neighbor = 0 if c == (self.cell_count - 1) else c + 1
            neighborhood: str  = str(self.cells[left_neighbor]) + str(self.cells[c]) + str(self.cells[right_neighbor])
            self.__next_state[c] = self.ruleset[neighborhood]
        for c in range(0, self.cell_count):
            self.cells[c] = self.__next_state[c]
        return

    def print_iteration(self) -> None:
        """Print an iteration by representing each cell in the state as a color"""
        if self.iteration == 0:
            self.show_properties()

        print(str(self.iteration).ljust(3) + " ", end='')
        [print(self.colors[0], end = '') if c == 0 else
         print(self.colors[1], end = '') if c == 1 else
         print(self.colors[2], end = '') for c in self.cells]
        print("")

        if self.iteration == self.t:
            print('    ' + ''.join([str(c) for c in self.cells]))
        return

    # smaller helper functions:

    def to_ternary(self, decimal: int) -> str:
        """Converts a decimal number to its ternary representation (string with length 3)"""
        return np.base_repr(decimal, base=3)

    def binary_ruleset(self, rule: int) -> typing.Dict[str, int]:
        """Creates a ruleset for a binary CA rule"""
        rule_bin: str = format(rule, '08b')
        binaries: list = [format(i, '03b') for i in range(7, -1, -1)]
        return {binaries[i]:int(rule_bin[i]) for i in range(8)}

    def ternary_ruleset(self, rule: int) -> typing.Dict[str, int]:
        """Creates a ruleset for a ternary CA rule"""
        rule_ter: str = str(self.to_ternary(rule)).zfill(27)
        ternaries: typing.List[str] = [str(self.to_ternary(i)).zfill(3) for i in range(26, -1, -1)]
        return {ternaries[i]:int(rule_ter[i]) for i in range(27)}

    def get_ruleset(self, rule: int) -> typing.Dict[str, int]:
        """Gets a ruleset which is either binary of ternary depending on the rule number"""
        if rule != None:
            return self.binary_ruleset(rule) if rule <= 255 else self.ternary_ruleset(rule)
        return {'': 0}
    
    def get_colors(self, ansi0: str, ansi1: str, ansi2: str) -> typing.Tuple[str]:
        """
        Gets the actual colors for the background coloring based on ANSI arguments
        :param ansi0: ANSI number representing the color that cells identical to 0 will be
        :param ansi1: ANSI number representing the color that cells identical to 1 will be
        :param ansi2: ANSI number representing the color that cells identical to 2 will be
        :return colors: tuple with the colors
        """
        color0 = '\033[0;' + ansi0 + 'm \033[0m'
        color1 = '\033[0;' + ansi1 + 'm \033[0m'
        color2 = '\033[0;' + ansi2 + 'm \033[0m'
        return color0, color1, color2
    
    def set_colors(self) -> None:
        """Sets the colors of the visualization"""
        # 40 black, 41 red, 42 green, 43 yellow, 44 blue, 45 purple, 46 cyan, 47 white
        ansi0: str = '40' # black
        ansi1: str = '47' # white
        ansi2: str = '41' # red
        self.colors: typing.Tuple(str) = self.get_colors(ansi0, ansi1, ansi2) # colors are set
        return

    def show_properties(self) -> None:
        """Short utility function to output the cellular automaton's attributes"""
        print('cell count: ' + str(self.cell_count))
        print('rule number: ' + str(self.rule_number))
        print('    ' + ''.join([str(c) for c in self.c0]))
        return
