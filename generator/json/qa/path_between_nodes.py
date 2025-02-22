"""
*Question_11*: "If some when wants to go to Node 1, and satrting from node 2, what is the path he need to be taken?"
*Direction*: What is the path of the one node to the other node?
"""

import json
import random
import os
import logging

def read_json_file(file_path):
    """Read JSON file and return its contents"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format"
    except Exception as e:
        return f"Error: {str(e)}"

def get_nodes_with_relationships(data):
    """Find all nodes with their parent and children relationships"""
    nodes = {}
    
    def traverse(obj, parent_name=None, level=0):
        if isinstance(obj, dict):
            current_name = None
            node_type = None
            
            # Try to get the name and type of current node
            for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                if name_key in obj:
                    current_name = obj[name_key]
                    node_type = name_key.replace(' Name', '').lower()
                    break
            
            if current_name:
                if current_name not in nodes:
                    nodes[current_name] = {
                        'type': node_type,
                        'parent': parent_name,
                        'children': set(),
                        'level': level
                    }
                if parent_name:
                    nodes[parent_name]['children'].add(current_name)
                
                # Continue traversing with current node as parent
                for v in obj.values():
                    traverse(v, current_name, level + 1)
            else:
                # Continue traversing with same parent
                for v in obj.values():
                    traverse(v, parent_name, level)
                    
        elif isinstance(obj, list):
            for item in obj:
                traverse(item, parent_name, level)
    
    traverse(data)
    return nodes

def find_path_between_nodes(nodes, start_name, end_name):
    """Find path from start node to end node through common ancestors"""
    if start_name not in nodes or end_name not in nodes:
        return None
    
    # Find path from start to root
    path_to_root = []
    current = start_name
    while current:
        path_to_root.append(current)
        current = nodes[current]['parent']
    
    # Find path from end to root
    path_from_end = []
    current = end_name
    while current:
        path_from_end.append(current)
        current = nodes[current]['parent']
    
    # Find common ancestor
    common_ancestor = None
    for node in path_to_root:
        if node in path_from_end:
            common_ancestor = node
            break
    
    if not common_ancestor:
        return None
    
    # Build complete path
    # From start to common ancestor
    final_path = []
    for node in path_to_root:
        final_path.append(node)
        if node == common_ancestor:
            break
    
    # From common ancestor to end (reversed)
    reverse_path = []
    for node in path_from_end:
        if node == common_ancestor:
            break
        reverse_path.append(node)
    
    final_path.extend(reversed(reverse_path))
    return final_path

def gen_answer_path_between_nodes(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """Generate question about path between any two nodes"""
    try:
        # Read the JSON file
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "dataset",
            "JSON",
            "dataset",
            f"{scenario}.json"
        )
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            
        # Get available layers for this scenario
        if get_available_layers_func is None:
            logging.error("get_available_layers_func not provided")
            return None, None
            
        scenario_info = get_available_layers_func(scenario)
        if not scenario_info:
            logging.error(f"No layer information found for scenario: {scenario}")
            return None, None
            
        available_layers = scenario_info["layers"]
        
        # Get all nodes with their relationships
        nodes = get_nodes_with_relationships(data)
        if len(nodes) < 2:
            return None, None
        
        # Try to find valid node pairs
        max_attempts = 100
        for _ in range(max_attempts):
            # Select two different nodes
            node1_name, node2_name = random.sample(list(nodes.keys()), 2)
            
            # Find path between nodes
            path = find_path_between_nodes(nodes, node1_name, node2_name)
            
            if path and len(path) > 2:  # Ensure path has at least one intermediate node
                node1_type = nodes[node1_name]['type']
                node2_type = nodes[node2_name]['type']
                
                # Form question and answer
                question = f"If someone wants to go from the {node1_type} '{node1_name}' to the {node2_type} '{node2_name}', what path should they take?"
                answer = " -> ".join(path) if with_answer else None
                
                return question, answer
        
        return None, None
    except Exception as e:
        logging.error(f"Error in gen_answer_path_between_nodes: {str(e)}")
        return None, None

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_path_between_nodes("university_structure_large_01", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)