from .base import BasicEvaluator

class PaperEvaluator(BasicEvaluator):
    def __init__(self, key = 'answer', strip_symbols = '\'"'):
            super().__init__(key, strip_symbols)
            
    def contextual_qa(self, source, target):
        return self.hit_rate(source, target, sep=',')
    
    def disordered_section(self, source, target):
        return self.hit_rate(source, target, sep=',')
    
    def outline_extraction(self, source, target):
        source = source.replace('\\n', '\n').replace('\n', ',')
        target = target.replace('\\n', '\n').replace('\n', ',')
        return self.hit_rate(source, target, sep=',')