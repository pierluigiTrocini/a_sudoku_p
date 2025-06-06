from embasp.specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from embasp.platforms.desktop.desktop_handler import DesktopHandler
from embasp.languages.asp.asp_mapper import ASPMapper
from embasp.languages.asp.asp_input_program import ASPInputProgram
from embasp.base.option_descriptor import OptionDescriptor
from embasp.languages.asp.answer_sets import AnswerSets
from utility import *

import logging

N = 9

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s'
)
        
class AIManager:
    SOLVER_PATH: str = './dlv-2.1'
    ASP_RULES_PATH: str = './rules.dlv'
    INPUT_FILE_PATH: str = './input.txt'

    def __init__(self):
        self.grid = []
        with open(self.INPUT_FILE_PATH, 'r') as file:
            for line in file:
                # Convert each line into a list of integers
                row = list(map(int, line.split()))
                self.grid.append(row)

    def show_grid_terminal(self, grid):
        for i in range(N):
            for j in range(N):
                print( f" {grid[i][j] if grid[i][j] != 0 else '*'} ", end = '' )
                if (j+1) % 3 == 0:
                    print('|', end='')

            if (i+1) % 3 == 0 and (i+1) != 9:
                print(f"\n{'_'*29}")
            
            print()

        print(f"\n{'_'*29}")

    def generate_facts(self) -> list:
        facts = []

        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] != 0:
                    facts.append(Cell(row = (i + 1), col = (j + 1), value = self.grid[i][j]))

        return facts
    

    def dlv_call(self) -> str:
        self.show_grid_terminal(grid = self.grid)

        try:
            handler: DesktopHandler = DesktopHandler(DLV2DesktopService(self.SOLVER_PATH))

            ASPMapper.get_instance().register_class(Cell)
            ASPMapper.get_instance().register_class(Solution)

            inputProgram: ASPInputProgram = ASPInputProgram()
            inputProgram.add_files_path(self.ASP_RULES_PATH)
            inputProgram.add_objects_input(self.generate_facts())
            handler.add_option(OptionDescriptor("--no-facts"))
            handler.add_option(OptionDescriptor("-n1"))

            handler.add_program(inputProgram)

            answerSets: AnswerSets = handler.start_sync()

            solution = [[0] * 9 for _ in range(9)]

            for atom in answerSets.get_answer_sets().pop().get_atoms():
                if isinstance(atom, Solution):
                    solution[atom.row - 1][atom.col - 1] = atom.value
            
            self.show_grid_terminal(grid = solution)

        finally:
            inputProgram.clear_all()

if __name__ == '__main__':
    AIManager().dlv_call()
