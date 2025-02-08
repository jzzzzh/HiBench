from .base import BasicEvaluator

class CodeEvaluator(BasicEvaluator):
    
    def __init__(self, key = 'answer', strip_symbols = '\'"'):
            super().__init__(key, strip_symbols)
            
    def SpaceComplexity(self, source, target):
        return self.string_match(source, target)
    def TimeComplexity(self, source, target):
        return self.string_match(source, target)
    def CodeMissing(self, source, target):
        return self.string_match(source, target)