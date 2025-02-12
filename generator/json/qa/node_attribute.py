"""
**Question_5**: "What is the university name?"
**Direction**: What info is on leaf x.
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
        """Check if dictionary represents a leaf node with attributes"""
        # All possible attribute keys in our dataset
        attribute_keys = {
            # University level
            'University',
            # Faculty level
            'Faculty Name',
            # Department level
            'Department Name',
            # Program level
            'Program Name',
            # Course level
            'Course Name',
            # Person level
            'Name', 'Title', 'Student ID'
        }
        
        # Check if it has any attributes we care about
        has_attributes = any(key in d for key in attribute_keys)
        
        # Special handling for different structure types
        if 'Program Name' in d and len(d) == 1:  # For mid_2/large_2 structure
            return True
        if 'Name' in d and 'Title' in d:  # For lecturer nodes
            return True
        if 'Name' in d and 'Student ID' in d:  # For student nodes
            return True
        
        # Check if it's a leaf node (no nested structures except known attributes)
        has_children = any(
            isinstance(v, (dict, list)) and k not in ['Lecturers', 'Students']
            for k, v in d.items()
        )
        
        return has_attributes and not has_children

    def traverse(obj, ancestry=None):
        if ancestry is None:
            ancestry = []
            
        if isinstance(obj, dict):
            # Get the name/identifier for this level
            current_name = None
            for name_key in [
                'University',
                'Faculty Name',
                'Department Name',
                'Program Name',
                'Course Name',
                'Name'
            ]:
                if name_key in obj:
                    current_name = obj[name_key]
                    break
                    
            if current_name:
                ancestry = ancestry + [current_name]
                
            if is_leaf_dict(obj):
                leaf_nodes.append((obj, ancestry))
            
            # Always traverse children
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    traverse(v, ancestry)
                    
        elif isinstance(obj, list):
            for item in obj:
                traverse(item, ancestry)
    
    traverse(data)
    return leaf_nodes

def gen_answer_node_attribute(scenario: str, with_answer: bool = True, get_available_layers_func=None):
    """Generate question about node attributes"""
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
        
        # Get all leaf nodes with their ancestry
        leaf_nodes = get_leaf_nodes_with_ancestry(data)
        if not leaf_nodes:
            logging.error(f"No leaf nodes found in {scenario}")
            return None, None
        
        # Randomly select a leaf node
        selected_node, ancestry = random.choice(leaf_nodes)
        
        # Get attributes based on node type
        if 'Program Name' in selected_node and len(selected_node) == 1:
            # For mid_2/large_2 structure, ask about program name
            question = f"What is the name of the program in {ancestry[-2]}?"
            answer = selected_node['Program Name'] if with_answer else None
            return question, answer
        
        # For other structures, get all simple attributes
        attributes = [k for k, v in selected_node.items() 
                     if isinstance(v, (str, int, float)) and k != 'University']
        
        if len(attributes) < 2:
            logging.error(f"Not enough attributes in node for {scenario}")
            return None, None
        
        # Randomly select two different attributes
        attr1, attr2 = random.sample(attributes, 2)
        
        # Form the context string from ancestry
        context = " in ".join(reversed(ancestry[:-1])) if len(ancestry) > 1 else ""
        
        # Form question and answer
        if context:
            if 'Student ID' in selected_node:
                question = f"What is the {attr2} of the student {selected_node[attr1]} who is in {context}?"
            elif 'Title' in selected_node:
                question = f"What is the {attr2} of the lecturer {selected_node[attr1]} who is in {context}?"
            else:
                question = f"What is the {attr2} of {selected_node[attr1]} in {context}?"
        else:
            question = f"What is the {attr2} of {selected_node[attr1]}?"
        
        answer = selected_node[attr2] if with_answer else None
        
        return question, answer
    except Exception as e:
        logging.error(f"Error generating answer for {scenario}: {str(e)}")
        return None, None

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_node_attribute("company", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)