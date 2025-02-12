"""
*Question_8*: "If the department is coming to find the student, what is the path he need to be taken?"
*Direction*: What is the path of the one node to the another node.
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

def get_nodes_with_children(data):
    """Find all nodes with their children and level information"""
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

def find_path_down(data, start_name, target_name, current_path=None):
    """Find path from a higher node down to a lower node"""
    if current_path is None:
        current_path = []
        
    if isinstance(data, dict):
        # Check if this is the start node
        current_node_name = None
        for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
            if name_key in data and data[name_key] == start_name:
                current_node_name = data[name_key]
                break
                
        if current_node_name:
            # If we found the start node, begin collecting the path
            path = find_target_from_start(data, target_name, [data])
            if path:
                return path
            return None
            
        # If we haven't found the start node yet, keep searching
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
                            path = find_path_down(item, start_name, target_name, current_path + [data])
                            if path:
                                return path
            elif keys in data:
                if isinstance(data[keys], list):
                    for item in data[keys]:
                        path = find_path_down(item, start_name, target_name, current_path + [data])
                        if path:
                            return path
                else:
                    path = find_path_down(data[keys], start_name, target_name, current_path + [data])
                    if path:
                        return path
    return None

def find_target_from_start(data, target_name, current_path):
    """Find target node starting from the start node"""
    if isinstance(data, dict):
        # Check if this is the target node
        for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
            if name_key in data and data[name_key] == target_name:
                return current_path + [data]
                
        # Search in child nodes
        for value in data.values():
            if isinstance(value, (dict, list)):
                path = find_target_from_start(value, target_name, current_path + [data])
                if path:
                    return path
    elif isinstance(data, list):
        for item in data:
            path = find_target_from_start(item, target_name, current_path)
            if path:
                return path
    return None

def get_random_nodes_different_levels(data, available_layers):
    """Get two random nodes from different levels where one is above the other"""
    nodes_by_level = {level: [] for level in available_layers}
    
    def collect_nodes(obj, current_level=0):
        if isinstance(obj, dict):
            # Get node name if it exists
            for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                if name_key in obj:
                    nodes_by_level[current_level].append((obj[name_key], name_key))
                    break
            
            # Continue searching in child nodes with incremented level
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    collect_nodes(value, current_level + 1)
        elif isinstance(obj, list):
            for item in obj:
                collect_nodes(item, current_level)
    
    collect_nodes(data)
    
    # Filter out empty levels and sort by level
    valid_levels = [(level, nodes) for level, nodes in nodes_by_level.items() if nodes]
    if len(valid_levels) < 2:
        return None
        
    # Select two different levels where one is higher than the other
    level1, level2 = random.sample(range(len(valid_levels)), 2)
    if level1 > level2:
        level1, level2 = level2, level1
        
    # Select random nodes from these levels
    node1 = random.choice(nodes_by_level[level1])
    node2 = random.choice(nodes_by_level[level2])
    
    return node1, node2

def gen_answer_path_up_to_down(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """Generate question about path from a higher node down to a lower node"""
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
        
        # Get two random nodes from different levels
        nodes = get_random_nodes_different_levels(data, available_layers)
        if not nodes:
            logging.error(f"Could not find suitable nodes in {scenario}")
            return None, None
            
        (start_name, _), (target_name, _) = nodes
        
        # Find path from start to target
        path = find_path_down(data, start_name, target_name)
        if not path:
            logging.error(f"Could not find path from {start_name} to {target_name}")
            return None, None
            
        # Generate question
        question = f"What is the path from {start_name} down to {target_name}?"
        
        # Generate answer
        if with_answer:
            path_names = []
            for node in path:
                for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                    if name_key in node:
                        path_names.append(node[name_key])
                        break
            answer = " -> ".join(path_names)
        else:
            answer = None
            
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_answer_path_up_to_down: {str(e)}")
        return None, None

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_path_up_to_down("university_structure_large_01", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)