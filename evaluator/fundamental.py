from .base import BasicEvaluator


class FundamentalEvaluator(BasicEvaluator):
    
    def __init__(self, key = 'answer', strip_symbols = '\'"'):
        super().__init__(key, strip_symbols)
        
    def add_node(self, source, target, represent_mode, sep: str = ',', remove_blank: bool = True):
        if represent_mode == 'edge':
            return self.list_match(source, target, sep, remove_blank)
        else:
            return self.hierarchical_structure_match(source, target)
    
    def all_ancestor(self, source, target, sep: str = ',', remove_blank: bool = True):
        if target == 'None':
            return self.string_match(source, target)
        else:
            return self.list_match(source, target, sep, remove_blank)
    
    def all_children(self, source, target, sep: str = ',', remove_blank: bool = True):
        if target == 'None':
            return self.string_match(source, target)
        else:
            return self.list_match(source, target, sep, remove_blank)
    
    def common_ancestor(self, source, target):
        return self.string_match(source, target)
    
    def isomorphic(self, source, target):
        return self.string_match(source, target)
    
    def remove_node(self, source, target, represent_mode, sep: str = ',', remove_blank: bool = True):
        if target == 'No edges':
            return self.string_match(source, target)
        else:
            if represent_mode == 'edge':
                return self.list_match(source, target, sep, remove_blank)
            else:
                return self.hierarchical_structure_match(source, target)
    
    def node_depth(self, source, target):
        return self.string_match(source, target)
    
    def leaf(self, source, target):
        return self.string_match(source, target)
    
    def root(self, source, target):
        return self.string_match(source, target)
    
    def balance(self, source, target):
        return self.string_match(source, target)
    
    def prefix_traversal(self, source, target, sep: str = ',', remove_blank: bool = True):
        return self.list_match(source, target, sep, remove_blank)
    
    def infix_traversal(self, source, target, sep: str = ',', remove_blank: bool = True):
        return self.list_match(source, target, sep, remove_blank)
    
    def postfix_traversal(self, source, target, sep: str = ',', remove_blank: bool = True):
        return self.list_match(source, target, sep, remove_blank)
    
    def traversal_order_verification(self, source, target):
        return self.string_match(source, target)
    
    def mirror_tree(self, source, target, represent_mode, sep: str = ',', remove_blank: bool = True):
        if represent_mode == 'edge':
            return self.list_match(source, target, sep, remove_blank)
        else:
            return self.hierarchical_structure_match(source, target)