"""
*Question_8*: "If the department is coming to find the student, what is the path he need to be taken?"
*Direction*: What is the path of the one node to the another node.
"""

import json
import random
import os

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

def find_path_down(nodes, start_name, end_name):
    """Find path from start node down to end node if it exists"""
    if start_name not in nodes or end_name not in nodes:
        return None
        
    # Only proceed if start node is at least 2 levels higher than end node
    if nodes[end_name]['level'] - nodes[start_name]['level'] < 2:
        return None
    
    def find_path(current, target, path):
        if current == target:
            return path
            
        if current not in nodes:
            return None
            
        for child in nodes[current]['children']:
            new_path = find_path(child, target, path + [child])
            if new_path:
                return new_path
        return None
    
    return find_path(start_name, end_name, [start_name])

def get_nodes_by_level(nodes):
    """Group nodes by their level"""
    levels = {}
    for name, info in nodes.items():
        level = info['level']
        if level not in levels:
            levels[level] = []
        levels[level].append(name)
    return levels

def gen_answer_type_8(scenario: str, with_answer: bool = True):
    """Generate questions about paths from higher to lower level nodes"""
    file_path = os.path.join(os.path.dirname(__file__), "..", "dataset", f"{scenario}.json")
    data = read_json_file(file_path)
    
    if isinstance(data, str):  # Error occurred
        return None, None
    
    # Get all nodes with their relationships
    nodes = get_nodes_with_children(data)
    if len(nodes) < 2:
        return None, None
    
    # Group nodes by level
    levels_dict = get_nodes_by_level(nodes)
    levels = sorted(levels_dict.keys())
    
    # Try to find valid path between nodes
    max_attempts = 100
    for _ in range(max_attempts):
        # Select two levels with at least one level between them
        valid_level_pairs = [(l1, l2) for l1 in levels for l2 in levels if l2 - l1 >= 2]
        if not valid_level_pairs:
            continue
            
        start_level, end_level = random.choice(valid_level_pairs)
        
        # Select random nodes from these levels
        start_name = random.choice(levels_dict[start_level])
        end_name = random.choice(levels_dict[end_level])
        
        # Find path from start down to end
        path = find_path_down(nodes, start_name, end_name)
        
        if path:
            start_type = nodes[start_name]['type']
            end_type = nodes[end_name]['type']
            
            # Form question and answer
            question = f"If someone from the {start_type} '{start_name}' needs to find the {end_type} '{end_name}', what path should they take?"
            answer = " → ".join(path) if with_answer else None
            
            return question, answer
    
    return None, None

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_type_8("university_structure_large_01", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)