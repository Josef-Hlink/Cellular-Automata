from cellularautomata import CellularAutomata
import typing # just good practice
import ast # for being able to read the list straight from the txt file
import numpy as np

def main():
    with open('interesting rules.txt') as file:
        try:
            rules: typing.List[int] = [int(line.rstrip()) for line in file]
        except ValueError:
            print('Please take a look at the file named: "interesting rules.txt" and check if there\'s only integers there')
            return
    
    for rule in rules:
        # initialize the automaton with this rule
        automaton: CellularAutomata = CellularAutomata(rule_number = rule)
        # set number of iterations
        iterations: int = 299

        # get list of starting conditions from the file
        with open('starting condition.txt', 'r') as file:
            conditions: typing.List[list] = [ast.literal_eval(line.rstrip()) for line in file]
        
        # choose a starting condition from the list of conditions
        condition: typing.List[int] = conditions[0] # choose a starting condition from the list of conditions
        result: typing.List[int] = automaton(c0 = condition, t = iterations)
    return

def test():
    with open('starting condition.txt', 'r') as file:
        conditions: typing.List[list] = [ast.literal_eval(line.rstrip()) for line in file]
    rule: int = np.random.randint(0, 10000000)
    automaton: CellularAutomata = CellularAutomata(rule_number = rule)
    automaton(conditions[0], 299)

if __name__ == '__main__':
    main()