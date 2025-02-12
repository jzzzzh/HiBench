"""
Question 8: "What is the path from X down to Y?"
Direction: Given two nodes in the hierarchy where one is an ancestor of the other, return the full path (names)
from the ancestor node down to the descendant node.
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
    Recursively traverse the JSON tree and collect nodes.
    Each collected entry is a tuple: (name, node, level, path)
      - name: the extracted name of the node.
      - node: the dictionary representing the node.
      - level: the depth of the node.
      - path: a list of nodes from the root to this node.
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
        # Recurse into every dict or list field
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                collect_nodes(value, new_path, current_level + 1, collected)
    elif isinstance(data, list):
        for item in data:
            collect_nodes(item, current_path, current_level, collected)
    
    return collected

def get_valid_ancestor_descendant_pair(data):
    """
    Returns a random valid pair (parent, descendant) where:
      - Each is a tuple: (name, node, level, path)
      - The parent's node appears in the descendant's ancestry path, and
        the descendant is at a strictly lower level (deeper) than the parent.
    Returns None if no valid pair is found.
    """
    all_nodes = collect_nodes(data)
    candidates = []
    for i in range(len(all_nodes)):
        for j in range(len(all_nodes)):
            if i == j:
                continue
            parent_name, parent_node, parent_level, parent_path = all_nodes[i]
            descendant_name, descendant_node, descendant_level, descendant_path = all_nodes[j]
            if descendant_level > parent_level and parent_node in descendant_path:
                candidates.append((all_nodes[i], all_nodes[j]))
    if not candidates:
        return None
    return random.choice(candidates)

def gen_answer_path_up_to_down(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """
    Generate a question and answer about the path from a higher-level (ancestor) node to a lower-level node.
    Returns:
      question: e.g., "What is the path from X down to Y?"
      answer: a string of node names separated by " -> " representing the sub-path from X to Y.
    """
    try:
        # Determine the file path. Adjust folder structure as needed.
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "dataset", "JSON", "dataset", f"{scenario}.json"
        )
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        pair = get_valid_ancestor_descendant_pair(data)
        if not pair:
            logging.error(f"Could not find a valid ancestor-descendant pair in scenario: {scenario}")
            return None, None
        
        (parent_name, parent_node, parent_level, parent_path), (descendant_name, descendant_node, descendant_level, descendant_path) = pair
        
        # Find the index in the descendant's ancestry path where the parent appears.
        try:
            parent_index = descendant_path.index(parent_node)
        except ValueError:
            logging.error("Parent node not found in descendant's path (unexpected).")
            return None, None
        
        # The sub-path from parent to descendant:
        subpath = descendant_path[parent_index:]
        path_names = []
        for node in subpath:
            name = get_node_name(node)
            if name:
                path_names.append(name)
        if not path_names:
            logging.error("No names found in the computed path.")
            return None, None
        
        question = f"What is the path from {parent_name} down to {descendant_name}?"
        answer = " -> ".join(path_names) if with_answer else None
        
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_answer_path_up_to_down: {str(e)}")
        return None, None

# Example usage for testing:
if __name__ == "__main__":
    # Replace 'your_scenario' with your dataset name (without .json extension).
    q, a = gen_answer_path_up_to_down("university_structure_large_1", with_answer=True)
    print("Question:", q)
    print("Answer:", a)