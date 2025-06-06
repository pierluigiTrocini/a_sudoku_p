from embasp.languages.predicate import Predicate

class Cell(Predicate):
    predicate_name = 'cell'

    def __init__(self, row = None, col = None, value = None):
        Predicate.__init__(self,[('row', int), ('col', int), ('value', int)])

        self.row = row
        self.col = col
        self.value = value
    
    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col
    
    def get_value(self):
        return self.value
    
    def set_row(self, r: int):
        self.row = r

    def set_col(self, c: int):
        self.col = c
    
    def set_value(self, v: int):
        self.value = v
    
    def __str__(self):
        return f'{self.predicate_name}({self.row}, {self.col}, {self.value}).'

class Solution(Cell):
    predicate_name = 'solution'

    def __init__(self, row=None, col=None, value=None):
        super().__init__(row, col, value)