"""
*Question_6*: "What are the names of the departments in the university?"
*Direction*: What are the names of the nodes in level x.
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

def get_nodes_at_level(data, target_level, current_level=0):
    """Get all nodes at a specific level with their names"""
    nodes = []
    
    # Special handling at the root: if the root contains "Faculties", use that
    if current_level == 0 and isinstance(data, dict) and "Faculties" in data:
        return get_nodes_at_level(data["Faculties"], target_level, current_level + 1)
    
    if current_level == target_level:
        # Get node name based on level
        name_keys = {
            1: 'Faculty Name',
            2: 'Department Name',
            3: 'Program Name',
            4: 'Course Name',
            5: 'Name'  # For both Lecturers and Students
        }
        
        key = name_keys.get(current_level)
        if key and key in data:
            nodes.append(data[key])
        return nodes
    
    # Mapping for nodes in the subtree (starting from Faculty level)
    subtree_keys = {
        1: 'Departments',    # For a Faculty node, its children are in "Departments"
        2: 'Programs',       # For a Department node, its children are in "Programs"
        3: 'Courses',        # For a Program node, its children are in "Courses"
        4: ['Lecturers', 'Students']  # For a Course node, its children are in these lists
    }
    
    if isinstance(data, dict):
        current_key = subtree_keys.get(current_level)
        if isinstance(current_key, list):
            for key in current_key:
                if key in data:
                    for item in data[key]:
                        nodes.extend(get_nodes_at_level(item, target_level, current_level + 1))
        elif current_key and current_key in data:
            if isinstance(data[current_key], list):
                for item in data[current_key]:
                    nodes.extend(get_nodes_at_level(item, target_level, current_level + 1))
            else:
                nodes.extend(get_nodes_at_level(data[current_key], target_level, current_level + 1))
    elif isinstance(data, list):
        for item in data:
            nodes.extend(get_nodes_at_level(item, target_level, current_level))
    
    return nodes

def get_level_name(level):
    """Get the appropriate name for each level"""
    level_names = {
        0: "organization",
        1: "faculties",
        2: "departments",
        3: "programs",
        4: "courses"
    }
    return level_names.get(level, "units")

def gen_answer_level_nodes(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """Generate question about listing all nodes at a specific level"""
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
        layer_names = scenario_info["names"]
        
        # Randomly select a layer
        layer_index = random.choice(available_layers)
            
        # Get all nodes at the selected level
        nodes = get_nodes_at_level(data, layer_index)
        if not nodes:
            logging.error(f"No nodes found at level {layer_index} for {scenario}")
            return None, None
            
        # Generate question
        question = f"List all {layer_names[layer_index]} in the {data['University']}."
        answer = ", ".join(nodes) if with_answer else None
        
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_answer_level_nodes: {str(e)}")
        return None, None

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_level_nodes("university_structure_large_01", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)