from .base import BasicEvaluator

class JsonEvaluator(BasicEvaluator):
    def __init__(self, key = 'answer', strip_symbols = '\'"'):
            super().__init__(key, strip_symbols)
            
    def child_count(self, source, target):
        return self.number_match(source, target)
    
    def node_depth(self, source, target):
        return self.number_match(source, target)
    
    def level_count(self, source, target):
        return self.number_match(source, target)
    
    def node_attribute(self, source, target):
        return self.string_match(source, target)
    
    def level_nodes(self, source, target):
        return self.list_match(source, target, sep=',')
    
    def path_between_nodes(self, source, target):
        return self.string_match(source, target)
    
    def path_down_to_up(self, source, target):
        return self.string_match(source, target)
    
    def path_up_to_down(self, source, target):
        return self.string_match(source, target)
    
    def shared_ancestor_same_level(self, source, target):
        return self.string_match(source, target)
    
    def shared_ancestor_diff_level(self, source, target):
        return self.string_match(source, target)
