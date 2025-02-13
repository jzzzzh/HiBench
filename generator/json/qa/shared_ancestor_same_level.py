"""
Question 9: Common Ancestor (Same Level)
" What is the common ancestor of X and Y?"
Direction: Given two nodes on the same level in the hierarchy, return the name of their deepest common ancestor.
"""

import json
import os
import random
import logging

def get_node_name(node):
    """Return the node's name by checking common key options."""
    for key in ['University', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name', 'Name']:
        if key in node:
            return node[key]
    return None

def collect_nodes(data, current_path=None, current_level=0, collected=None):
    """
    Recursively collect nodes from the JSON tree.
    Each entry in collected is a tuple: (name, node, level, path)
    The path is a list of nodes (from root to the current node).
    """
    if current_path is None:
        current_path = []
    if collected is None:
        collected = []
    
    if isinstance(data, dict):
        node_name = get_node_name(data)
        new_path = current_path + [data]
        if node_name:
            collected.append((node_name, data, current_level, new_path))
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                collect_nodes(value, new_path, current_level + 1, collected)
    elif isinstance(data, list):
        for item in data:
            collect_nodes(item, current_path, current_level, collected)
    
    return collected

def find_common_ancestor(path1, path2):
    """
    Given two ancestry paths (lists of node dicts from root to node),
    return the deepest common node (as dict) or None.
    """
    common = None
    for n1, n2 in zip(path1, path2):
        if n1 == n2:
            common = n1
        else:
            break
    return common

def find_proper_common_ancestor(path1, path2):
    """
    Return the deepest proper common ancestor that is not equal to either target node.
    """
    common_list = []
    for n1, n2 in zip(path1, path2):
        if n1 == n2:
            common_list.append(n1)
        else:
            break
    if len(common_list) >= 2:
        return common_list[-2]
    return None

def gen_answer_shared_ancestor_same_level(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """
    Generate a question for two nodes at the same level.
    The question is:
       "What is the common ancestor of X and Y?"
    and the answer is the name of their deepest shared ancestor.
    """
    try:
        # Form the JSON file path
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "dataset", "JSON", "dataset", f"{scenario}.json"
        )
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Collect all nodes
        all_nodes = collect_nodes(data)
        if not all_nodes or len(all_nodes) < 2:
            logging.error("Insufficient nodes found in the dataset.")
            return None, None
        
        # Group nodes by level
        nodes_by_level = {}
        for entry in all_nodes:
            level = entry[2]
            nodes_by_level.setdefault(level, []).append(entry)
        
        # Exclude the root level (often level 0) if it has only one node
        valid_levels = [lvl for lvl, nodes in nodes_by_level.items() if len(nodes) >= 2 and lvl > 0]
        if not valid_levels:
            logging.error("No level found with at least two nodes for a same level comparison.")
            return None, None
        
        # Randomly select one level from the valid ones
        chosen_level = random.choice(valid_levels)
        node_pair = random.sample(nodes_by_level[chosen_level], 2)
        
        name1, _, lvl, path1 = node_pair[0]
        name2, _, lvl, path2 = node_pair[1]
        
        common_ancestor = find_common_ancestor(path1, path2)
        if not common_ancestor:
            logging.error(f"Could not determine a common ancestor for {name1} and {name2}.")
            return None, None
        
        # Ensure that the common ancestor is not identical to either node.
        if common_ancestor == node_pair[0][1] or common_ancestor == node_pair[1][1]:
            proper_ancestor = find_proper_common_ancestor(path1, path2)
            if not proper_ancestor:
                logging.error(f"No proper common ancestor (non-self) found for {name1} and {name2}.")
                return None, None
            common_ancestor = proper_ancestor
        
        ancestor_name = get_node_name(common_ancestor)
        if not ancestor_name:
            logging.error("Common ancestor does not have a name.")
            return None, None
        
        question = f"What is the common ancestor of {name1} and {name2}?"
        answer = ancestor_name if with_answer else None
        
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_answer_shared_ancestor_same_level: {str(e)}")
        return None, None

# Example usage:
if __name__ == "__main__":
    # Replace 'your_scenario' with an actual scenario filename (without .json)
    q, a = gen_answer_shared_ancestor_same_level("university_structure_mid_1", with_answer=True)
    print("Question:", q)
    print("Answer:", a)