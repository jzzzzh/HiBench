"""
**Question_4**: "Does Dr. Peter teach Student Jason?"
**Direction**: Does Node A belong to Node B.
To do 
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

def check_node_belongs_to(data, node1, node2):
    """Check if node2 is a grandchild of node1"""
    def find_node_distance(obj, start_node, target_node, current_depth=0):
        if isinstance(obj, dict):
            # Check if current node is the start_node
            if any(value == start_node for value in obj.values()):
                # Search for target_node in descendants
                result = find_target_depth(obj, target_node, 0)
                return result if result is not None else -1
                
            # Continue searching for start_node
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    result = find_node_distance(value, start_node, target_node, current_depth)
                    if result >= 0:
                        return result
        elif isinstance(obj, list):
            for item in obj:
                result = find_node_distance(item, start_node, target_node, current_depth)
                if result >= 0:
                    return result
        return -1

    def find_target_depth(obj, target_node, depth):
        if isinstance(obj, dict):
            if any(value == target_node for value in obj.values()):
                return depth
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    result = find_target_depth(value, target_node, depth + 1)
                    if result is not None:
                        return result
        elif isinstance(obj, list):
            for item in obj:
                result = find_target_depth(item, target_node, depth)
                if result is not None:
                    return result
        return None

    distance = find_node_distance(data, node1, node2)
    return distance == 2  # True if node2 is exactly a grandchild of node1

def get_all_nodes(data):
    """Get all named nodes from the JSON structure"""
    nodes = []
    
    def traverse(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if 'Name' in key and isinstance(value, str):
                    nodes.append(value)
                if isinstance(value, (dict, list)):
                    traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(data)
    return list(set(nodes))  # Remove duplicates

def select_two_random_nodes(json_data):
    """Select two random nodes from the structure and check if they belong to each other"""
    if isinstance(json_data, str):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            return "Error: Invalid JSON format"
    else:
        return "Error: Input must be a JSON string"

    # Get all nodes
    all_nodes = get_all_nodes(data)
    
    if len(all_nodes) < 2:
        return "Error: Not enough nodes in the structure"

    # Select two different random nodes
    node1, node2 = random.sample(all_nodes, 2)

    # Check if node2 is a descendant of node1
    belongs_to = check_node_belongs_to(data, node1, node2)

    return node1, node2, belongs_to

def find_relationship(data, node1_name, node2_name):
    """Find the relationship between two nodes"""
    def find_path_to_node(data, target_name, current_path=None):
        if current_path is None:
            current_path = []
            
        if isinstance(data, dict):
            # Check if this is the target node
            for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                if name_key in data and data[name_key] == target_name:
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
                                path = find_path_to_node(item, target_name, current_path + [data])
                                if path:
                                    return path
                elif keys in data:
                    if isinstance(data[keys], list):
                        for item in data[keys]:
                            path = find_path_to_node(item, target_name, current_path + [data])
                            if path:
                                return path
                    else:
                        path = find_path_to_node(data[keys], target_name, current_path + [data])
                        if path:
                            return path
        return None

    # Find paths to both nodes
    path1 = find_path_to_node(data, node1_name)
    path2 = find_path_to_node(data, node2_name)
    
    if not path1 or not path2:
        return None
        
    # Find common ancestor
    common_ancestor = None
    for node1, node2 in zip(path1, path2):
        if node1 == node2:
            common_ancestor = node1
        else:
            break
            
    if not common_ancestor:
        return None
        
    # Determine relationship based on paths
    def get_node_type(node):
        for key in ['Faculty Name', 'Department Name', 'Program Name', 'Course Name', 'Name']:
            if key in node:
                return key.replace(' Name', '').lower()
        return None
        
    node1_type = get_node_type(path1[-1])
    node2_type = get_node_type(path2[-1])
    
    return {
        'node1_type': node1_type,
        'node2_type': node2_type,
        'common_ancestor': common_ancestor,
        'path1': path1,
        'path2': path2
    }

def get_random_nodes(data, available_layers):
    """Get two random nodes from the hierarchy"""
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
    if len(nodes) < 2:
        return None
        
    return random.sample(nodes, 2)

def gen_answer_node_relationship(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """Generate question about relationship between two nodes"""
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
        
        # Get two random nodes
        nodes = get_random_nodes(data, available_layers)
        if not nodes:
            logging.error(f"Could not find enough nodes in {scenario}")
            return None, None
            
        node1_name, _ = nodes[0]
        node2_name, _ = nodes[1]
        
        # Find relationship between nodes
        relationship = find_relationship(data, node1_name, node2_name)
        if not relationship:
            logging.error(f"Could not determine relationship between nodes")
            return None, None
            
        # Generate question
        question = f"What is the relationship between {node1_name} and {node2_name}?"
        
        # Generate answer
        if with_answer:
            common_ancestor_name = None
            for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                if name_key in relationship['common_ancestor']:
                    common_ancestor_name = relationship['common_ancestor'][name_key]
                    break
                    
            answer = (f"({common_ancestor_name}")
        else:
            answer = None
            
        return question, answer
        
    except Exception as e:
        logging.error(f"Error in gen_answer_node_relationship: {str(e)}")
        return None, None

if __name__ == "__main__":
    count = 0
    questions_answers = []
    
    while count < 10:
        question, answer = gen_answer_node_relationship(
            scenario="company", 
            with_answer=True
        )
        count += int(answer)
        
        if answer:
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            print(count)
            
            # Format each Q&A as a dictionary
            qa_dict = {
                "question": question,
                "answer": answer
            }
            questions_answers.append(qa_dict)

    # Save to JSON file with proper formatting
    with open('company.json', 'w', encoding='utf-8') as f:
        json.dump(questions_answers, f, indent=2, ensure_ascii=False)
 