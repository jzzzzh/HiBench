"""
*Question_7*: "If student need to find the department, what the path he need to be taken"
*Direction*: What is the path of one node to the other node (these two nodes are in different layers)?
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

def get_nodes_with_parent(data):
    """Find all nodes with their parent information"""
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
                        'level': level
                    }
                
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

def find_path_up(data, node_name, current_path=None):
    """Find path from a node up to the root"""
    if current_path is None:
        current_path = []
        
    if isinstance(data, dict):
        # Check if this is the target node
        for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
            if name_key in data and data[name_key] == node_name:
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
        for level, keys in level_keys.items():
            if isinstance(keys, list):
                for key in keys:
                    if key in data:
                        for item in data[key]:
                            path = find_path_up(item, node_name, current_path + [data])
                            if path:
                                return path
            elif keys in data:
                if isinstance(data[keys], list):
                    for item in data[keys]:
                        path = find_path_up(item, node_name, current_path + [data])
                        if path:
                            return path
                else:
                    path = find_path_up(data[keys], node_name, current_path + [data])
                    if path:
                        return path
    return None

def get_random_leaf_node(data, available_layers):
    """Get a random leaf node from the hierarchy"""
    leaf_nodes = []
    
    def collect_leaf_nodes(obj):
        if isinstance(obj, dict):
            is_leaf = True
            # Check if this is a leaf node
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    is_leaf = False
                    break
                    
            if is_leaf:
                for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                    if name_key in obj:
                        leaf_nodes.append((obj[name_key], name_key))
                        break
            
            # Continue searching in child nodes
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    collect_leaf_nodes(value)
        elif isinstance(obj, list):
            for item in obj:
                collect_leaf_nodes(item)
    
    collect_leaf_nodes(data)
    if leaf_nodes:
        return random.choice(leaf_nodes)
    return None

def gen_answer_path_down_to_up(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """Generate question about path from a leaf node up to root"""
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
        
        # Get a random leaf node
        node_info = get_random_leaf_node(data, available_layers)
        if not node_info:
            logging.error(f"Could not find a leaf node in {scenario}")
            return None, None
            
        node_name, _ = node_info
        
        # Find path up to root
        path = find_path_up(data, node_name)
        if not path:
            logging.error(f"Could not find path for node {node_name}")
            return None, None
            
        # Generate question
        question = f"What is the path from {node_name} up to the {data['University']}?"
        
        # Generate answer
        if with_answer:
            path_names = []
            for node in reversed(path):
                for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                    if name_key in node:
                        path_names.append(node[name_key])
                        break
            answer = " -> ".join(path_names)
        else:
            answer = None
            
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_answer_path_down_to_up: {str(e)}")
        return None, None

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_path_down_to_up("university_structure_large_01", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)