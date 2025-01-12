# Normal Hierarchical Structure Prompt
def leaf_prompt(structure_text, node):
    common_prompt = f'Given the hierarchical structure {structure_text}, is node {str(node)} a leaf node?'
    answer_pattern = 'Return the result in JSON format directly as {"answer": true} if it is a leaf node, or {"answer": false} if it is not. Do not provide details of the process.'
    return common_prompt + "\n" + answer_pattern

def root_prompt(structure_text):
    common_prompt = f'Given the hierarchical structure {structure_text}, which node is the root?'
    answer_pattern = 'Return the result in JSON format directly as {"answer": 1}, where 1 is the node ID. Please do not feedback the detailed process.'
    return common_prompt + "\n" + answer_pattern
    
def node_depth_prompt(structure_text, node):
    common_prompt = f"Given the hierarchical structure {structure_text}, determine the depth of the node {node} within the structure, where the root node is assigned a depth of 1."
    answer_pattern = 'Return the result in JSON format directly as {"answer": 1}, where 1 is the depth of the given node. Please do not feedback the detailed process.'
    return common_prompt + "\n" + answer_pattern

def common_ancestor_prompt(structure_text, nodes):
    common_prompt = f"Given the hierarchical structure {structure_text}, determine the lowest common ancestor of the nodes {nodes[0]} and {nodes[1]} within the structure."
    answer_pattern = 'Return the result in JSON format directly as {"answer": 1}, where 1 is the node ID. Please do not feedback the detailed process.'
    return common_prompt + "\n" + answer_pattern

def isomorphic_prompt(structure_text, another_structure_text):
    common_prompt = f'Given the hierarchical structure {structure_text} and another hierarchical structure: {another_structure_text}, please decide whether the given two structure are isomorphic or not.'
    answer_pattern = 'Return the result in JSON format directly as {"answer": true} if they are isomorphic or {"answer": false} if not. Please do not feedback the detailed process.'
    return common_prompt + "\n" + answer_pattern

def add_node_prompt(structure_text, nodes):
    common_prompt = f"Given the hierarchical structure {structure_text}, add a node {nodes[0]} as a child to the node {nodes[1]} in the given structure. Output the updated structure following the input structure format."
    answer_pattern = 'Please return the updated structure in JSON format directly as {"answer": <new structure>}. Do not provide any details of the process.'
    return common_prompt + "\n" + answer_pattern

def remove_node_prompt(structure_text, node):
    common_prompt = f'Given the hierarchical structure {structure_text}, please remove the node '+ str(node) + ' from the given structure. Output the updated structure following the input structure format.'
    answer_pattern = 'Please return the updated structure in JSON format directly as {"answer": <new structure>}. Do not provide any details of the process.'
    return common_prompt + "\n" + answer_pattern

# Binary Structure Prompt
def check_balance_prompt(structure_text, node):
    common_prompt = f'Given the hierarchical structure {structure_text}, is node {str(node)} a leaf node?'
    answer_pattern = 'Return the result in JSON format directly as {"answer": true} if it is a leaf node, or {"answer": false} if it is not. Do not provide details of the process.'
    return common_prompt + "\n" + answer_pattern