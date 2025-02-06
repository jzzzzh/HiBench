from .base import BasicEvaluator

class PaperEvaluator(BasicEvaluator):
    def __init__(self, key = 'answer', strip_symbols = '\'"'):
            super().__init__(key, strip_symbols)
    def contextual_qa(self, source, target):
        return self.string_match(source, target)
    def disordered_section(self, source, target):
        return self.string_match(source, target)
    def outline_extraction(self, source, target):
        return self.string_match(source, target)