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

def get_available_layers(scenario: str):
    """Get available layers for each scenario"""
    layers = {
        "university_structure_small": {
            "layers": [0, 1, 2],
            "names": ["Faculties", "Departments", "Programs"]
        },
        "university_structure_medium_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            # Use plural keys to match the JSON ("Courses", "Lecturers", "Students")
            "names": ["Faculties", "Departments", "Programs", "Courses", "Lecturers", "Students"]
        },
        "university_structure_medium_2": {
            "layers": [0, 1, 2],
            "names": ["Faculties", "Departments", "Programs"]
        },
        "university_structure_large_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            # IMPORTANT: match plural keys in the JSON
            "names": ["Faculties", "Departments", "Programs", "Courses", "Lecturers", "Students"]
        },
        "university_structure_large_2": {
            "layers": [0, 1, 2],
            "names": ["Faculties", "Departments", "Programs"]
        },
        # Bullshit versions have same structure as their counterparts
        "university_bullshit_structure_small": {
            "layers": [0, 1, 2],
            "names": ["Faculties", "Departments", "Programs"]
        },
        "university_bullshit_structure_medium_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculties", "Departments", "Programs", "Courses", "Lecturers", "Students"]
        },
        "university_bullshit_structure_medium_2": {
            "layers": [0, 1, 2],
            "names": ["Faculties", "Departments", "Programs"]
        },
        "university_bullshit_structure_large_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculties", "Departments", "Programs", "Courses", "Lecturers", "Students"]
        },
        "university_bullshit_structure_large_2": {
            "layers": [0, 1, 2],
            "names": ["Faculties", "Departments", "Programs"]
        }
    }
    
    if scenario not in layers:
        logging.error(f"No layer information found for scenario: {scenario}")
        return None
        
    logging.info(f"Found layers for {scenario}: {layers[scenario]}")
    return layers.get(scenario)

def get_nodes_at_level(data, target_level, current_level=0, node_type=None):
    """Get all nodes at a specific level with their names."""
    nodes = []
    
    # Handle root level
    if current_level == 0 and isinstance(data, dict) and "Faculties" in data:
        return get_nodes_at_level(data["Faculties"], target_level, current_level + 1, node_type)
    
    # If we've reached target level, extract names
    if current_level == target_level:
        if isinstance(data, dict):
            if node_type == "Student":
                if "Name" in data:
                    nodes.append(data["Name"])
            elif node_type == "Lecturer":
                if "Name" in data:
                    nodes.append(data["Name"])
            else:
                name_keys = {
                    1: "Faculty Name",
                    2: "Department Name",
                    3: "Program Name",
                    4: "Course Name"
                }
                if current_level in name_keys and name_keys[current_level] in data:
                    nodes.append(data[name_keys[current_level]])
        return nodes

    # Traverse the hierarchy
    if isinstance(data, dict):
        next_level = None
        if current_level == 0:
            next_level = data.get("Faculties", [])
        elif current_level == 1:
            next_level = data.get("Departments", [])
        elif current_level == 2:
            next_level = data.get("Programs", [])
        elif current_level == 3:
            # For Lecturers, we need to go through Courses
            if node_type == "Lecturer":
                next_level = data.get("Courses", [])
            elif node_type == "Student":
                next_level = data.get("Students", [])
            else:
                next_level = data.get("Courses", [])
        elif current_level == 4:
            # For Lecturers at course level
            if node_type == "Lecturer":
                next_level = data.get("Lecturers", [])

        if next_level:
            if isinstance(next_level, list):
                for item in next_level:
                    nodes.extend(get_nodes_at_level(item, target_level, current_level + 1, node_type))
            else:
                nodes.extend(get_nodes_at_level(next_level, target_level, current_level + 1, node_type))
                
    elif isinstance(data, list):
        for item in data:
            nodes.extend(get_nodes_at_level(item, target_level, current_level, node_type))
    
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
    """Generate question about listing all nodes at a specific level with retry mechanism"""
    max_retries = 10
    
    for attempt in range(max_retries):
        try:
            file_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                "dataset",
                "JSON",
                "dataset",
                f"{scenario}.json"
            )
            
            with open(file_path, 'r') as file:
                data = json.load(file)
                
            if get_available_layers_func is None:
                logging.error("get_available_layers_func not provided")
                continue
                
            scenario_info = get_available_layers_func(scenario)
            if not scenario_info:
                logging.error(f"No layer information found for scenario: {scenario}")
                continue
                
            available_layers = scenario_info["layers"]
            layer_names = scenario_info["names"]
            
            # Select a random layer
            layer_index = random.choice(available_layers)
            layer_name = layer_names[layer_index]

            # Set the correct level and node type based on the layer
            if layer_name == "Students":
                effective_level = 4
                node_type = "Student"
            elif layer_name == "Lecturers":
                effective_level = 5  # Changed: Lecturers are at level 5 (under Courses)
                node_type = "Lecturer"
            else:
                effective_level = layer_index + 1
                node_type = None

            # Get nodes
            nodes = get_nodes_at_level(data, effective_level, node_type=node_type)
            if not nodes:
                logging.warning(f"No nodes found at level {effective_level} for {scenario} with layer {layer_name}, retrying...")
                continue
                
            question = f"List all {layer_name} in the {data['University']}."
            answer = ", ".join(nodes) if with_answer else None
            
            if question and answer:
                return question, answer
                
        except Exception as e:
            logging.error(f"Error in gen_answer_level_nodes (attempt {attempt + 1}): {str(e)}")
            continue
    
    # Fallback to Departments if all retries fail
    try:
        layer_index = 1
        layer_name = "Departments"
        effective_level = 2
        nodes = get_nodes_at_level(data, effective_level)
        if nodes:
            question = f"List all {layer_name} in the {data['University']}."
            answer = ", ".join(nodes) if with_answer else None
            return question, answer
    except Exception as e:
        logging.error(f"Final fallback attempt failed: {str(e)}")
    
    return None, None

if __name__ == "__main__":
    successful_generations = 0
    attempts = 0
    max_attempts = 10
    
    while successful_generations < 3 and attempts < max_attempts:
        question, answer = gen_answer_level_nodes(
            "university_structure_medium_1", 
            with_answer=True, 
            get_available_layers_func=get_available_layers
        )
        
        if question and answer:
            print("\nQuestion:", question)
            print("Answer:", answer)
            successful_generations += 1
        
        attempts += 1