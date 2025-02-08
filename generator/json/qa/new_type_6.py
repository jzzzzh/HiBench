"""
*Question_6*: "What are the names of the departments in the university?"
*Direction*: What are the names of the nodes in level x.
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

def get_nodes_at_level(data, target_level):
    """Find all node names at a specific level"""
    nodes = []
    
    def traverse(obj, current_level=0):
        if isinstance(obj, dict):
            # Try to get the name of current level
            for name_key in ['Name', 'Faculty Name', 'Department Name', 'Program Name', 'Course Name']:
                if name_key in obj:
                    if current_level == target_level:
                        nodes.append(obj[name_key])
                    break
            
            # Continue traversing
            for v in obj.values():
                traverse(v, current_level + 1)
                    
        elif isinstance(obj, list):
            for item in obj:
                traverse(item, current_level)
    
    traverse(data)
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

def gen_answer_type_6(scenario: str, with_answer: bool = True):
    """Generate questions about names of nodes at a specific level"""
    file_path = os.path.join(os.path.dirname(__file__), "..", "dataset", f"{scenario}.json")
    data = read_json_file(file_path)
    if isinstance(data, str):  # Error occurred
        return None, None
    
    # Randomly select a level (1 to 3 are most meaningful - faculty, department, program)
    level = random.randint(1, 3)
    level_name = get_level_name(level)
    
    # Get all nodes at the selected level
    nodes = get_nodes_at_level(data, level)
    if not nodes:
        return None, None
    
    # Form question
    question = f"What are the names of the {level_name} in the {scenario}?"
    answer = ", ".join(sorted(nodes)) if with_answer else None
    
    return question, answer

# Example usage
if __name__ == "__main__":
    for _ in range(3):  # Generate 3 example questions
        question, answer = gen_answer_type_6("university_structure_large_01", with_answer=True)
        print("\nQuestion:", question)
        print("Answer:", answer)