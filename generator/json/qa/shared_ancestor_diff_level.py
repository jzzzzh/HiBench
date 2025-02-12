"""
*Question_10*: "What is the closest shared upper-level compoent between Jason and Department of Computing? "
*Direction*: What is the closest shared upper-level compoent between two nodes in different level.
"""

import json
import random
import os
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
            # Only add if the node has a name
            collected.append((node_name, data, current_level, new_path))
        # Recurse into each key where the value is a dict or list
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
    return the deepest common node (as dict) or None if they do not share any.
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
    Return the deepest common node that is a proper ancestor (i.e. not equal to 
    either of the target nodes). If the common ancestry set has only one node, then
    no proper common ancestor exists.
    """
    common_list = []
    for n1, n2 in zip(path1, path2):
        if n1 == n2:
            common_list.append(n1)
        else:
            break
    # If at least two nodes are common then use the next-to-last common node.
    if len(common_list) >= 2:
        return common_list[-2]
    return None

def gen_answer_shared_ancestor_diff_level(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """
    Generate a question for two nodes at different levels.
    The question is:
       "What is the common ancestor of X and Y?"
    and the answer is the name of their deepest shared ancestor.
    """
    try:
        # Form the file path (adjust this as needed for your project structure)
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "dataset", "JSON", "dataset", f"{scenario}.json"
        )
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Collect all nodes from the dataset
        all_nodes = collect_nodes(data)
        if not all_nodes or len(all_nodes) < 2:
            logging.error("Insufficient nodes found in the dataset.")
            return None, None
        
        # Group nodes by their level
        nodes_by_level = {}
        for entry in all_nodes:
            level = entry[2]
            nodes_by_level.setdefault(level, []).append(entry)
        
        # Get levels that actually exist and sort them
        levels = sorted(nodes_by_level.keys())
        if len(levels) < 2:
            logging.error("Not enough different levels available for diff level selection.")
            return None, None
        
        # Randomly select one level for one node and a different level for the other node.
        level1, level2 = random.sample(levels, 2)
        # For clarity, let level1 be the higher level (smaller number)
        if level1 > level2:
            level1, level2 = level2, level1
        
        node1 = random.choice(nodes_by_level[level1])
        node2 = random.choice(nodes_by_level[level2])
        
        name1, _, lvl1, path1 = node1
        name2, _, lvl2, path2 = node2
        
        common_ancestor = find_common_ancestor(path1, path2)
        if not common_ancestor:
            logging.error(f"Could not determine a common ancestor for {name1} and {name2}.")
            return None, None
        
        # Ensure the common ancestor is not one of the target nodes.
        if common_ancestor == node1 or common_ancestor == node2:
            proper_ancestor = find_proper_common_ancestor(path1, path2)
            if not proper_ancestor:
                logging.error(f"No proper common ancestor (non-self) found for {name1} and {name2}.")
                return None, None
            common_ancestor = proper_ancestor
        
        ancestor_name = get_node_name(common_ancestor)
        if not ancestor_name:
            logging.error("Common ancestor does not have a name.")
            return None, None
        
        # Generate question string (omit the level details for clarity)
        question = f"What is the common ancestor of {name1} and {name2}?"
        answer = ancestor_name if with_answer else None
        
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_answer_shared_ancestor_diff_level: {str(e)}")
        return None, None

# Example usage:
if __name__ == "__main__":
    # Replace 'your_scenario' with an actual scenario filename (without .json)
    q, a = gen_answer_shared_ancestor_diff_level("university_structure_large_1", with_answer=True)
    print("Question:", q)
    print("Answer:", a)