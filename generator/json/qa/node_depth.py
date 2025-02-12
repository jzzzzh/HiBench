"""
**Question_2**: "Which level does the node 'Computing Dept' in?"
**Direction**: Depth of a node.

"""

import json
import random
import os
import logging


def read_json_file(file_path):
    """Read JSON file and return its contents"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format"
    except Exception as e:
        return f"Error: {str(e)}"


def find_node_and_containers(data, target_name):
    """Find a node, its parent container and sibling count"""
    result = {
        'parent_type': None,
        'sibling_count': 0,
        'parent_name': None
    }

    def traverse(obj, parent=None, container_type=None):
        if isinstance(obj, dict):
            # Store potential container name
            container_name = None
            for key in obj.keys():
                if 'Name' in key:
                    container_name = obj[key]
                    break

            # Check for name fields
            for key, value in obj.items():
                if isinstance(value, str) and value == target_name:
                    if parent and isinstance(parent, list):
                        result['parent_type'] = container_type
                        result['sibling_count'] = len(parent)
                        result['parent_name'] = container_name
                        return True

            # Continue searching in nested structures
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    if traverse(value, obj, key):
                        return True

        elif isinstance(obj, list):
            # Check if target is in this list
            for item in obj:
                if isinstance(item, dict):
                    for value in item.values():
                        if value == target_name:
                            result['parent_type'] = container_type
                            result['sibling_count'] = len(obj)
                            if parent and isinstance(parent, dict):
                                for p_key, p_value in parent.items():
                                    if 'Name' in p_key and isinstance(p_value, str):
                                        result['parent_name'] = p_value
                                        break
                            return True

            # Continue searching in nested structures
            for item in obj:
                if traverse(item, obj, container_type):
                    return True
        return False

    traverse(data)
    return result


def get_all_layer_types(data):
    """Identify all layer types in the JSON structure"""
    layer_types = set()

    def traverse(obj):
        if isinstance(obj, dict):
            for key in obj.keys():
                # if isinstance(obj[key], list) and key not in ['Students', 'Lecturers']:
                if isinstance(obj[key], list):
                    layer_types.add(key)
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(data)
    return sorted(list(layer_types))


def get_nodes_from_layer(data, layer_type):
    """Get all nodes from a specific layer"""
    nodes = []

    def traverse(obj):
        if isinstance(obj, dict):
            if layer_type in obj:
                if isinstance(obj[layer_type], list):
                    for item in obj[layer_type]:
                        if isinstance(item, dict):
                            for key, value in item.items():
                                if 'Name' in key and isinstance(value, str):
                                    nodes.append(value)
                                    break
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(data)
    return list(set(nodes))  # Remove duplicates


def select_random_node_by_layer_index(json_data, layer_index=None):
    """Select a random node from a layer specified by index"""
    # Load JSON data
    if isinstance(json_data, str):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            return "Error: Invalid JSON format"
    else:
        return "Error: Input must be a JSON string"

    # Get all layer types
    layer_types = get_all_layer_types(data)
    '''
        print("Available layers:")
    for i, layer in enumerate(layer_types):
        print(f"{i}: {layer}")
    '''


    # Validate layer_index
    if layer_index is None:
        return "Please specify a layer index"
    if not (0 <= layer_index < len(layer_types)):
        return f"Layer index must be between 0 and {len(layer_types) - 1}"

    # Get the layer type for the specified index
    layer_type = layer_types[layer_index]
    info_layer = layer_types[layer_index]
    # Get all nodes from specified layer
    nodes = get_nodes_from_layer(data, layer_type)

    if not nodes:
        return f"No nodes found in layer: {layer_type}"

    # Randomly select a node
    selected_node = random.choice(nodes)

    # Find node's container and count siblings
    info = find_node_and_containers(data, selected_node)

    return selected_node, info['parent_type'], info['sibling_count'], info['parent_name'], info_layer


def get_node_depth(data, target_name, current_depth=0):
    """Find the depth of a specific node in the hierarchy"""
    if isinstance(data, dict):
        # Check if this is the target node
        for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
            if name_key in data and data[name_key] == target_name:
                return current_depth
        
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
                            depth = get_node_depth(item, target_name, current_depth + 1)
                            if depth is not None:
                                return depth
            elif keys in data:
                if isinstance(data[keys], list):
                    for item in data[keys]:
                        depth = get_node_depth(item, target_name, current_depth + 1)
                        if depth is not None:
                            return depth
                else:
                    depth = get_node_depth(data[keys], target_name, current_depth + 1)
                    if depth is not None:
                        return depth
    return None


def get_random_node(data, available_layers):
    """Get a random node from any valid layer"""
    nodes = []
    
    def collect_nodes(obj):
        if isinstance(obj, dict):
            # Get node name if it exists
            for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                if name_key in obj:
                    nodes.append((obj[name_key], name_key))
                    break
            
            # Continue searching in child nodes
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    collect_nodes(value)
        elif isinstance(obj, list):
            for item in obj:
                collect_nodes(item)
    
    collect_nodes(data)
    if nodes:
        return random.choice(nodes)
    return None


def gen_anwser_node_depth(scenario: str, with_answer: bool = True, layer_index: int = None, get_available_layers_func=None):
    """Generate question about the depth of a specific node"""
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
        
        # Get a random node
        node_info = get_random_node(data, available_layers)
        if not node_info:
            logging.error(f"No suitable nodes found in {scenario}")
            return None, None
            
        node_name, node_type = node_info
        
        # Get the depth of the selected node
        depth = get_node_depth(data, node_name)
        if depth is None:
            logging.error(f"Could not determine depth for node {node_name}")
            return None, None
            
        # Generate question
        question = f"What is the depth of {node_name} in the {data['University']}? (starting from 0)"
        answer = str(depth) if with_answer else None
        
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_anwser_node_depth: {str(e)}")
        return None, None


# Execute the function
if __name__ == "__main__":
    question, answer = gen_anwser_node_depth(scenario="company", with_answer=True)
    print(question, answer)
    """
    Available layers:
        0: Departments
        1: Divisions
        2: Employees
        3: Teams
    """
    # question, answer = gen_anwser_type_1("company")
    # print(question, answer)