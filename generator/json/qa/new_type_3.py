"""
**Question_3**: "How many departments does a university has?" 
**Direction**: How many nodes in level x.

"""

import json
import random
import os


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
    #return list(set(nodes))  # Remove duplicates
    return list(nodes)

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
    number_of_nodes = len(nodes) #Numebr of nodes in the layer
    #print("Debug print"+nodes) 
    if not nodes: 
        return f"No nodes found in layer: {layer_type}"

    # Randomly select a node
    selected_node = random.choice(nodes)

    # Find node's container and count siblings
    info = find_node_and_containers(data, selected_node)

    return selected_node, info['parent_type'], info['sibling_count'], info['parent_name'], info_layer,number_of_nodes


def gen_anwser_type_3(scenario: str, layer_index: int = None, with_answer: bool = True):
    """
    gen_anwser_type_3 generation type 2 quesiton as well as the answer
    :param scenario: the scenario of the question
    :param layer_index: the index of the layer (depth start with 0)
    :return: question, answer
    """ 
    def gen_question(scenario, layer_index):

        file_path = os.path.join(
        os.path.dirname(__file__), "..", "dataset", f"{scenario}.json")
        json_data = read_json_file(file_path)

        if isinstance(json_data, str) and not json_data.startswith("Error"):
            # Specify the layer index (the function will show available layers)
            _layer_index = layer_index  # Change this to select different layers
            result = select_random_node_by_layer_index(json_data, _layer_index)
#How many departments does a university has?
        if isinstance(result, tuple):
            selected_node, parent_type, sibling_count, parent_name, layer_name,number_of_nodes = result
            question = f"How many {parent_type} does {scenario} have?"
            if with_answer:
                answer = number_of_nodes
            else:
                answer = None
        else:
            print(json_data)
            question, answer = None, None
        
        return question, answer
        
    return gen_question(scenario, layer_index)


# Execute the function
if __name__ == "__main__":
    question, answer = gen_anwser_type_3(scenario="university", layer_index=0, with_answer=True)
    print(question, answer)
    # question, answer = gen_anwser_type_1("company")
    # print(question, answer)
