"""
**Question_5**: "What is the university name?"
**Direction**: What info is on leaf x.
To do 
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

def get_leaf_nodes_with_ancestry(data):
    """Find all leaf nodes with their complete ancestry path"""
    leaf_nodes = []
    
    def is_leaf_dict(d):
        """Check if dictionary contains only simple types"""
        return all(not isinstance(v, (dict, list)) for v in d.values())
    
    def traverse(obj, ancestry=None):
        if ancestry is None:
            ancestry = []
            
        if isinstance(obj, dict):
            # Try to get the name of current level if it exists
            current_name = None
            for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                if name_key in obj:
                    current_name = obj[name_key]
                    break
                    
            if current_name:
                ancestry = ancestry + [current_name]
                
            if is_leaf_dict(obj):
                leaf_nodes.append((obj, ancestry))
            else:
                for k, v in obj.items():
                    traverse(v, ancestry)
                    
        elif isinstance(obj, list):
            for item in obj:
                traverse(item, ancestry)
    
    traverse(data)
    return leaf_nodes

def gen_answer_node_attribute(scenario: str, with_answer: bool = True):
    """Generate questions about attributes of leaf nodes with ancestry context"""
    file_path = os.path.join(os.path.dirname(__file__), "..", "dataset", f"{scenario}.json")
    data = read_json_file(file_path)
    
    if isinstance(data, str):  # Error occurred
        return None, None
    
    # Get all leaf nodes with their ancestry
    leaf_nodes = get_leaf_nodes_with_ancestry(data)
    if not leaf_nodes:
        return None, None
    
    # Randomly select a leaf node
    selected_node, ancestry = random.choice(leaf_nodes)
    
    # Get all available attributes for the selected node
    attributes = list(selected_node.keys())
    if len(attributes) < 2:  # Need at least 2 attributes to form a question
        return None, None
    
    # Randomly select two different attributes
    attr1, attr2 = random.sample(attributes, 2)
    
    # Form the context string from ancestry
    context = " in ".join(reversed(ancestry[:-1])) if len(ancestry) > 1 else ""
    
    # Form question and answer
    if context:
        question = f"What is the {attr2} of {selected_node[attr1]} who is in {context}?"
    else:
        question = f"What is the {attr2} of {selected_node[attr1]}?"
    
    answer = selected_node[attr2] if with_answer else None
    
    return question, answer

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_node_attribute("company", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)