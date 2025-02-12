"""
Question_1: "How many subjects does Computing Dept have?"

Direction: How many node N2 does node N1 have.

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
    
    # Special handling for faculty level (root level)
    if 'Faculties' in data and isinstance(data['Faculties'], list):
        for faculty in data['Faculties']:
            if isinstance(faculty, dict) and faculty.get('Faculty Name') == target_name:
                result['parent_type'] = 'Faculties'
                result['sibling_count'] = len(data['Faculties'])
                result['parent_name'] = data.get('University')  # Get the university name
                return result
    
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
                #if isinstance(obj[key], list) and key not in ['Students', 'Lecturers']:
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
        return f"Layer index must be between 0 and {len(layer_types)-1}"
    
    # Get the layer type for the specified index
    layer_type = layer_types[layer_index]
    
    # Get all nodes from specified layer
    nodes = get_nodes_from_layer(data, layer_type)
    
    if not nodes:
        return f"No nodes found in layer: {layer_type}"
    
    # Randomly select a node
    selected_node = random.choice(nodes)
    
    # Find node's container and count siblings
    info = find_node_and_containers(data, selected_node)
    
    return selected_node, info['parent_type'], info['sibling_count'], info['parent_name']

def get_node_at_layer(data, target_layer, current_layer=0):
    """Get all nodes at a specific layer"""
    nodes = []
    
    if current_layer == target_layer:
        logging.debug(f"Found node at target layer {target_layer}: {data}")
        if isinstance(data, list):
            return [d if isinstance(d, dict) else {"Name": d} for d in data]
        elif isinstance(data, dict):
            return [data]
        elif isinstance(data, str):
            return [{"Name": data}]
        return [data]
    
    # Special handling at the root: if the root contains "Faculties", use that
    if current_layer == 0 and isinstance(data, dict) and "Faculties" in data:
        logging.debug("At root; recursing into 'Faculties' key.")
        return get_node_at_layer(data["Faculties"], target_layer, current_layer)

    # Mapping for nodes in the subtree (starting from Faculty level)
    subtree_keys = {
        0: 'Departments',    # For a Faculty node, its children are in "Departments"
        1: 'Programs',       # For a Department node, its children are in "Programs"
        2: 'Courses',        # For a Program node, its children are in "Courses"
        3: ['Lecturers', 'Students']  # For a Course node, its children are in these lists
    }

    if isinstance(data, dict):
        # For nodes at current_layer >= 0 in the subtree, use the subtree mapping.
        current_key = subtree_keys.get(current_layer)
        logging.debug(f"Looking for key {current_key} at subtree layer {current_layer}")
        if current_key:
            if isinstance(current_key, list):
                for key in current_key:
                    if key in data:
                        logging.debug(f"Found list key {key} at subtree layer {current_layer}")
                        for item in data[key]:
                            nodes.extend(get_node_at_layer(item, target_layer, current_layer + 1))
            else:
                if current_key in data:
                    logging.debug(f"Found key {current_key} at subtree layer {current_layer}")
                    if isinstance(data[current_key], list):
                        for item in data[current_key]:
                            nodes.extend(get_node_at_layer(item, target_layer, current_layer + 1))
                    else:
                        nodes.extend(get_node_at_layer(data[current_key], target_layer, current_layer + 1))
    elif isinstance(data, list):
        for item in data:
            nodes.extend(get_node_at_layer(item, target_layer, current_layer))
    return nodes

def count_children(node, tree_level):
    """Count direct children of a node when the node is at the given tree level.
    Here tree_level is the actual level in the JSON tree.
    Children are located at tree_level + 1"""
    if isinstance(node, dict):
        # Map tree-level numbers to their container keys
        layer_keys = {
            0: 'University',   # Level 0: University
            1: 'Faculties',    # Level 1: Faculties
            2: 'Departments',  # Level 2: Departments
            3: 'Programs',     # Level 3: Programs
            4: 'Courses',      # Level 4: Courses
            5: ['Lecturers', 'Students']  # Level 5: People
        }
        
        # Look for children at level tree_level + 1
        target_keys = layer_keys.get(tree_level + 1)
        if isinstance(target_keys, list):
            total_count = 0
            for key in target_keys:
                if key in node and isinstance(node[key], list):
                    total_count += len(node[key])
            return total_count
        elif target_keys in node:
            if isinstance(node[target_keys], list):
                return len(node[target_keys])
            else:
                return 1
    return 0

def get_nodes_at_level(data, target_level, current_level=0):
    """
    Recursively retrieve all nodes at a specified JSON tree level in our assumed structure.
    Levels:
      0: Root (data has keys "University" and "Faculties")
      1: Faculty nodes (inside "Faculties")
      2: Department nodes (inside "Departments")
      3: Program nodes (inside "Programs")
      4: Course nodes (inside "Courses")
      5: People nodes (inside "Lecturers" and "Students") - not used here.
    """
    nodes = []
    # If we are at the target level, return the current node(s)
    if current_level == target_level:
        if isinstance(data, list):
            return data
        else:
            return [data]
    
    # Special handling at the root: if the root contains "Faculties", then start there.
    if current_level == 0 and isinstance(data, dict) and "Faculties" in data:
        return get_nodes_at_level(data["Faculties"], target_level, current_level + 1)
    
    # Mapping from parent level to the key that holds its children
    children_keys_map = {
        1: "Departments",      # For Faculty nodes
        2: "Programs",         # For Department nodes
        3: "Courses",          # For Program nodes
        4: ["Lecturers", "Students"]  # For Course nodes
    }
    
    if isinstance(data, dict):
        if current_level in children_keys_map:
            key = children_keys_map[current_level]
            if isinstance(key, str):
                if key in data:
                    return get_nodes_at_level(data[key], target_level, current_level + 1)
            elif isinstance(key, list):
                for k in key:
                    if k in data:
                        nodes.extend(get_nodes_at_level(data[k], target_level, current_level + 1))
        else:
            # Fall back: try any list-valued child
            for value in data.values():
                if isinstance(value, (dict, list)):
                    nodes.extend(get_nodes_at_level(value, target_level, current_level + 1))
    elif isinstance(data, list):
        for item in data:
            nodes.extend(get_nodes_at_level(item, target_level, current_level))
    return nodes

def count_children_in_node(parent_node, parent_json_level):
    """
    Count direct children of a parent node, using our fixed hierarchy.
    Based on parent_json_level:
      - If parent_json_level == 1 (Faculty node), count items in "Departments".
      - If parent_json_level == 2 (Department node), count items in "Programs".
      - If parent_json_level == 3 (Program node), count items in "Courses".
      - If parent_json_level == 4 (Course node), count items in both "Lecturers" and "Students".
    """
    children_keys_map = {
        1: "Departments",
        2: "Programs",
        3: "Courses",
        4: ["Lecturers", "Students"]
    }
    key = children_keys_map.get(parent_json_level, None)
    if key is None:
        return 0
    count = 0
    if isinstance(key, str):
        children = parent_node.get(key, [])
        if isinstance(children, list):
            count = len(children)
        elif children:
            count = 1
    elif isinstance(key, list):
        for k in key:
            children = parent_node.get(k, [])
            if isinstance(children, list):
                count += len(children)
            elif children:
                count += 1
    return count

def gen_anwser_child_count(scenario: str, with_answer: bool = True, layer_index: int = None, get_available_layers_func=None):
    """
    Generate a child-count question based on the given scenario.
    
    The question is in the form:
       "How many {child_type}s are there in {parent_name}?"
    
    Mapping:
      - The scenario provides "layers" and "names". For example, if
            layers = [0,1,2,3,4,5] and names = ['Faculty','Department','Program','Course','Lecturer','Student']
        then user layer index 2 represents "Program" nodes.
      - Since the JSON root is level 0 ("University"), user layer index i is found at JSON level = i + 1.
      - The children of a node at JSON level (i+1) come from the appropriate key 
        ("Departments" for Faculty, "Programs" for Department, "Courses" for Program, etc.)
    """
    try:
        # Load the JSON file
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "dataset", "JSON", "dataset",
            f"{scenario}.json"
        )
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Get the scenario configuration (layers and names)
        if get_available_layers_func is None:
            logging.error("get_available_layers_func not provided")
            return None, None
        scenario_info = get_available_layers_func(scenario)
        if not scenario_info:
            logging.error(f"No layer information found for scenario: {scenario}")
            return None, None
        
        available_layers = scenario_info["layers"]     # e.g. [0,1,2,3,4,5]
        layer_names = scenario_info["names"]             # e.g. ['Faculty','Department','Program','Course','Lecturer','Student']
        
        # Validate layer_index: it must be less than the last layer because we want to count children
        if layer_index is None:
            valid_layers = [l for l in available_layers if l < len(available_layers) - 1]
            if not valid_layers:
                logging.error("No valid layers available for child counting")
                return None, None
            layer_index = random.choice(valid_layers)
        elif layer_index >= len(available_layers) - 1:
            logging.error("Provided layer_index is the last layer; cannot count children")
            return None, None
        
        # Convert user layer index to JSON tree level.
        # A user layer index of i corresponds to JSON level = i + 1.
        parent_json_level = layer_index + 1
        child_user_index = layer_index + 1  # Child type comes from this user index (child type = layer_names[layer_index+1])
        
        # Retrieve all parent nodes at JSON level (parent_json_level)
        parent_nodes = get_nodes_at_level(data, parent_json_level)
        if not parent_nodes:
            logging.error(f"No nodes found at JSON level {parent_json_level} for {scenario}")
            return None, None
        
        # Pick a random parent node
        parent_node = random.choice(parent_nodes)
        
        # Retrieve the parent's name.
        # Mapping of parent's JSON level to its name key:
        name_key_map = {
            1: "Faculty Name",
            2: "Department Name",
            3: "Program Name",
            4: "Course Name"
        }
        parent_name = None
        if parent_json_level in name_key_map:
            parent_name = parent_node.get(name_key_map[parent_json_level])
        if not parent_name:
            # Try fallback keys
            for key in ["Name", "Faculty Name", "Department Name", "Program Name", "Course Name"]:
                if key in parent_node:
                    parent_name = parent_node[key]
                    break
        if not parent_name:
            logging.error(f"Could not find name for node at JSON level {parent_json_level}")
            return None, None
        
        # Count children of the selected parent node using our mapping.
        child_count = count_children_in_node(parent_node, parent_json_level)
        
        # Determine the child type from the scenario configuration.
        child_type = layer_names[child_user_index]  # For example, if layer_index==2 then child_type = layer_names[3] == "Course"
        question = f"How many {child_type}s are there in {parent_name}?"
        answer = str(child_count) if with_answer else None
        
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_anwser_child_count: {str(e)}")
        return None, None

# Execute the function
if __name__ == "__main__":
    questions, answers = [], []
    # for i in range(10):
    #     question, answer = gen_anwser_child_count("university")
    #     questions.append(question)
    #     answers.append(answer)
    # with open("questions.txt", "w") as q_file:
    #     for question, answer in zip(questions, answers):
    #         q_file.write(question + "\n")
    #         q_file.write(str(answer) + "\n")
    #question, answer = gen_anwser_child_count(scenario="university", layer_index=5, with_answer=True)
    question, answer =  gen_anwser_child_count(scenario="university_structure_medium_1", with_answer=True, layer_index=2)
    print(question, answer)
    """
    Available layers:
        0: Courses
        1: Departments
        2: Faculties
        3: Lecturers
        4: Programs
        5: Students
    """
    #print(question, answer)