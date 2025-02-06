from .base import BasicEvaluator

class JsonEvaluator(BasicEvaluator):
    def __init__(self, key = 'answer', strip_symbols = '\'"'):
            super().__init__(key, strip_symbols)
    def Task1(self, source, target):
        return self.number_match(source, target)
    
    def Task2(self, source, target):
        return self.string_match(source, target)
    
    def Task3(self, source, target):
        return self.number_match(source, target)
    
    def Task4(self, source, target):
        return self.bool_match(source, target)
    
    def Task5(self, source, target):
         return self.string_match(source, target)