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


def get_nodes_by_key(data, layer_key):
    """Return all items found under `layer_key` at any depth."""
    results = []
    
    if isinstance(data, dict):
        for k, v in data.items():
            if k == layer_key and isinstance(v, list):
                # E.g. if k == "Students"
                results.extend(v)
            elif isinstance(v, (dict, list)):
                results.extend(get_nodes_by_key(v, layer_key))
                
    elif isinstance(data, list):
        for item in data:
            results.extend(get_nodes_by_key(item, layer_key))
    
    return results

def select_random_node_by_layer_index(json_data, layer_index=None):
    """Select a random node from a layer specified by index"""
    if isinstance(json_data, str):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            return "Error: Invalid JSON format"
    else:
        return "Error: Input must be a JSON string"

    # Get all layer types that exist in the JSON
    layer_types = get_all_layer_types(data)

    # Validate layer_index
    if layer_index is None:
        return "Please specify a layer index"
    if not (0 <= layer_index < len(layer_types)):
        return f"Layer index must be between 0 and {len(layer_types) - 1}"

    layer_type = layer_types[layer_index]
    nodes = get_nodes_by_key(data, layer_type)
    number_of_nodes = len(nodes)
    if not nodes: 
        return f"No nodes found in layer: {layer_type}"

    # Randomly select a node
    selected_node = random.choice(nodes)
    info = None
    # If selected_node has a 'Name' key, we can find the container info
    if isinstance(selected_node, dict):
        # For example, let's find if there's a 'Course Name', 'Lecturer Name', etc.
        for key, val in selected_node.items():
            if isinstance(val, str):
                # Attempt to find container info
                info = find_node_and_containers(data, val)
                if info['parent_type'] or info['parent_name']:
                    break

    return selected_node, (info['parent_type'] if info else None), \
           (info['sibling_count'] if info else 0), \
           (info['parent_name'] if info else None), \
           layer_type, number_of_nodes


def count_nodes_at_level(data, target_level, current_level=0):
    """Return how many items total are at target_level."""
    if current_level == target_level:
        if isinstance(data, list):
            return len(data)
        else:
            return 1  # It's a single dict or string
    
    total = 0
    if isinstance(data, dict):
        level_keys = {
            0: 'Faculties',
            1: 'Departments',
            2: 'Programs',
            3: 'Courses',
            4: 'Lecturers',
            5: 'Students'
        }
        current_key = level_keys.get(current_level)
        
        if current_key in data:
            value = data[current_key]
            if isinstance(value, list):
                for item in value:
                    total += count_nodes_at_level(item, target_level, current_level + 1)
            elif isinstance(value, dict):
                total += count_nodes_at_level(value, target_level, current_level + 1)
    
    elif isinstance(data, list):
        for item in data:
            total += count_nodes_at_level(item, target_level, current_level)
    
    return total


def get_nodes_at_level(data, target_level, current_level=0):
    """Get all nodes at a specific level (flattened)."""
    if current_level == target_level:
        # If we're exactly at the target level, return all items if it's a list
        # or a single-item list if it's a dict.
        if isinstance(data, list):
            return data
        else:
            return [data]
    
    nodes = []
    if isinstance(data, dict):
        # Map each level to a JSON key
        level_keys = {
            0: 'Faculties',
            1: 'Departments',
            2: 'Programs',
            3: 'Courses',
            4: 'Lecturers',
            5: 'Students'
        }
        current_key = level_keys.get(current_level)
        
        if current_key in data and isinstance(data[current_key], list):
            for item in data[current_key]:
                nodes.extend(get_nodes_at_level(item, target_level, current_level + 1))
        elif current_key in data and isinstance(data[current_key], dict):
            nodes.extend(get_nodes_at_level(data[current_key], target_level, current_level + 1))
    
    elif isinstance(data, list):
        for item in data:
            nodes.extend(get_nodes_at_level(item, target_level, current_level))
    
    return nodes


def gen_anwser_level_count(
    scenario: str,
    with_answer: bool = True,
    layer_index: int = None,
    get_available_layers_func=None
):
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
            return None, None
            
        scenario_info = get_available_layers_func(scenario)
        if not scenario_info:
            logging.error(f"No layer information found for scenario: {scenario}")
            return None, None
            
        available_layers = scenario_info["layers"]
        layer_names = scenario_info["names"]
        
        # If no layer_index given, pick randomly
        if layer_index is None:
            layer_index = random.choice(available_layers)
        
        # e.g. for layer_index=5 => "Students"
        layer_key = layer_names[layer_index]
        
        # Now retrieve all items matching that layer_key ANYWHERE in the JSON
        nodes = get_nodes_by_key(data, layer_key)
        node_count = len(nodes)
        
        question = f"How many {layer_key} are there in total in the {data['University']}?"
        answer = str(node_count) if with_answer else None
        
        return question, answer
    
    except Exception as e:
        logging.error(f"Error in gen_anwser_level_count: {str(e)}")
        return None, None


# Example usage
if __name__ == "__main__":
    # Force layer_index=3 to count "Courses" (plural!)
    question, answer = gen_anwser_level_count(
        scenario="university_structure_large_1",
        get_available_layers_func=get_available_layers,
        with_answer=True
    )
    print(question, answer)