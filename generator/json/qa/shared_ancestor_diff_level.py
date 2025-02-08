"""
*Question_10*: "What is the closest shared upper-level compoent between Jason and Department of Computing? "
*Direction*: What is the closest shared upper-level compoent between two nodes in different level.
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

def get_nodes_with_ancestry(data):
    """Find all nodes with their complete ancestry path"""
    nodes = {}
    
    def traverse(obj, ancestry=None, level=0):
        if ancestry is None:
            ancestry = []
            
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
                        'ancestry': ancestry + [current_name],
                        'level': level
                    }
                
                # Continue traversing with updated ancestry
                for v in obj.values():
                    traverse(v, ancestry + [current_name], level + 1)
            else:
                # Continue traversing with same ancestry
                for v in obj.values():
                    traverse(v, ancestry, level)
                    
        elif isinstance(obj, list):
            for item in obj:
                traverse(item, ancestry, level)
    
    traverse(data)
    return nodes

def find_closest_common_ancestor(nodes, node1_name, node2_name):
    """Find the closest common ancestor between two nodes"""
    if node1_name not in nodes or node2_name not in nodes:
        return None
        
    ancestry1 = nodes[node1_name]['ancestry']
    ancestry2 = nodes[node2_name]['ancestry']
    
    # Find common ancestors
    common_ancestors = []
    for a1, a2 in zip(ancestry1[:-1], ancestry2[:-1]):  # Exclude the nodes themselves
        if a1 != a2:
            break
        common_ancestors.append(a1)
    
    return common_ancestors[-1] if common_ancestors else None

def get_nodes_by_level(nodes):
    """Group nodes by their level"""
    levels = {}
    for name, info in nodes.items():
        level = info['level']
        if level not in levels:
            levels[level] = []
        levels[level].append(name)
    return levels

def gen_answer_shared_ancestor_diff_level(scenario: str, with_answer: bool = True):
    """Generate questions about closest common ancestor between nodes at different levels"""
    file_path = os.path.join(os.path.dirname(__file__), "..", "dataset", f"{scenario}.json")
    data = read_json_file(file_path)
    
    if isinstance(data, str):  # Error occurred
        return None, None
    
    # Get all nodes with their ancestry
    nodes = get_nodes_with_ancestry(data)
    if len(nodes) < 2:
        return None, None
    
    # Group nodes by level
    levels_dict = get_nodes_by_level(nodes)
    levels = sorted(levels_dict.keys())
    
    # Try to find valid node pairs
    max_attempts = 100
    for _ in range(max_attempts):
        # Select two different levels
        if len(levels) < 2:
            continue
        level1, level2 = random.sample(levels, 2)
        
        # Make sure we have nodes at both levels
        if not levels_dict[level1] or not levels_dict[level2]:
            continue
        
        # Select random nodes from these levels
        node1_name = random.choice(levels_dict[level1])
        node2_name = random.choice(levels_dict[level2])
        
        # Skip if we selected the same node
        if node1_name == node2_name:
            continue
        
        # Find their closest common ancestor
        common_ancestor = find_closest_common_ancestor(nodes, node1_name, node2_name)
        
        if common_ancestor:
            node1_type = nodes[node1_name]['type']
            node2_type = nodes[node2_name]['type']
            ancestor_type = nodes[common_ancestor]['type']
            
            # Form question and answer
            question = f"What is the closest shared {ancestor_type} between the {node1_type} '{node1_name}' and the {node2_type} '{node2_name}'?"
            answer = common_ancestor if with_answer else None
            
            return question, answer
    
    return None, None

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_shared_ancestor_diff_level("university_structure_large_01", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)