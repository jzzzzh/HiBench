"""
*Question_9*: "What is the closest shared upper-level compoent between Jason and Mike? "
*Direction*: What is the closest shared upper-level compoent between two nodes in same level.
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

def get_nodes_with_ancestry(data):
    """Find all nodes with their complete ancestry path"""
    nodes = {}
    
    def traverse(obj, ancestry=None, level=0):
        if ancestry is None:
            ancestry = []
            
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
                        'ancestry': ancestry + [current_name],
                        'level': level
                    }
                
                # Continue traversing with updated ancestry
                for v in obj.values():
                    traverse(v, ancestry + [current_name], level + 1)
            else:
                # Continue traversing with same ancestry
                for v in obj.values():
                    traverse(v, ancestry, level)
                    
        elif isinstance(obj, list):
            for item in obj:
                traverse(item, ancestry, level)
    
    traverse(data)
    return nodes

def find_common_ancestor(data, node1_name, node2_name, current_path=None):
    """Find the lowest common ancestor of two nodes at the same level"""
    if current_path is None:
        current_path = []
        
    if isinstance(data, dict):
        # Check if this is one of the target nodes
        current_node_name = None
        for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
            if name_key in data and data[name_key] in [node1_name, node2_name]:
                return current_path + [data]
                
        # Map level numbers to their container keys
        level_keys = {
            0: 'University',
            1: 'Faculties',
            2: 'Departments',
            3: 'Programs',
            4: 'Courses',
            5: ['Lecturers', 'Students']
        }
        
        # Search in child nodes
        paths = []
        for level, keys in level_keys.items():
            if isinstance(keys, list):
                for key in keys:
                    if key in data:
                        for item in data[key]:
                            path = find_common_ancestor(item, node1_name, node2_name, current_path + [data])
                            if path:
                                paths.append(path)
            elif keys in data:
                if isinstance(data[keys], list):
                    for item in data[keys]:
                        path = find_common_ancestor(item, node1_name, node2_name, current_path + [data])
                        if path:
                            paths.append(path)
                else:
                    path = find_common_ancestor(data[keys], node1_name, node2_name, current_path + [data])
                    if path:
                        paths.append(path)
                        
        if len(paths) == 2:  # Found both nodes
            # Find the lowest common ancestor
            min_len = min(len(paths[0]), len(paths[1]))
            common_ancestor = None
            for i in range(min_len):
                if paths[0][i] == paths[1][i]:
                    common_ancestor = paths[0][i]
                else:
                    break
            return [common_ancestor] if common_ancestor else None
            
        return paths[0] if len(paths) == 1 else None
    return None

def get_random_same_level_nodes(data, available_layers):
    """Get two random nodes from the same level"""
    nodes_by_level = {level: [] for level in available_layers}
    
    def collect_nodes(obj, current_level=0):
        if isinstance(obj, dict):
            # Get node name if it exists
            for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                if name_key in obj:
                    nodes_by_level[current_level].append((obj[name_key], name_key))
                    break
            
            # Continue searching in child nodes
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    collect_nodes(value, current_level + 1)
        elif isinstance(obj, list):
            for item in obj:
                collect_nodes(item, current_level)
    
    collect_nodes(data)
    
    # Find levels with at least 2 nodes
    valid_levels = [(level, nodes) for level, nodes in nodes_by_level.items() if len(nodes) >= 2]
    if not valid_levels:
        return None
        
    # Select a random level and two different nodes from it
    level, nodes = random.choice(valid_levels)
    node1, node2 = random.sample(nodes, 2)
    
    return node1, node2

def gen_answer_shared_ancestor_same_level(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """Generate question about finding common ancestor of two nodes at the same level"""
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
        
        # Get two random nodes from the same level
        nodes = get_random_same_level_nodes(data, available_layers)
        if not nodes:
            logging.error(f"Could not find suitable nodes in {scenario}")
            return None, None
            
        (node1_name, _), (node2_name, _) = nodes
        
        # Find their common ancestor
        ancestor_path = find_common_ancestor(data, node1_name, node2_name)
        if not ancestor_path:
            logging.error(f"Could not find common ancestor for {node1_name} and {node2_name}")
            return None, None
            
        # Get ancestor name
        ancestor_name = None
        for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
            if name_key in ancestor_path[0]:
                ancestor_name = ancestor_path[0][name_key]
                break
                
        if not ancestor_name:
            logging.error("Could not determine ancestor name")
            return None, None
            
        # Generate question
        question = f"What is the common ancestor of {node1_name} and {node2_name}?"
        answer = ancestor_name if with_answer else None
        
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_answer_shared_ancestor_same_level: {str(e)}")
        return None, None

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_shared_ancestor_same_level("university_structure_large_01", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)