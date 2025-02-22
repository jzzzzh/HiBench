from .base import BasicEvaluator

class FormulaEvaluator(BasicEvaluator):
    def __init__(self, key = 'answer', strip_symbols = '\'"'):
            super().__init__(key, strip_symbols)
    
    def calculate(self, source: str, target: str) -> bool:
        return self.number_match(source, target)
    
    def convert(self, source: str, target: str) -> bool:
        return self.string_match(source, target, skip=r'\s+|[\'"]')
    
    def equivalent(self, source: str, target: str) -> bool:
        return self.string_match(source, target)