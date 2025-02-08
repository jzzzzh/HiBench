"""
**Question_4**: "Does Dr. Peter teach Student Jason?"
**Direction**: Does Node A belong to Node B.
To do 
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

def gen_answer_node_relationship(scenario: str, with_answer: bool = True):
    """Generate questions about whether one node belongs to another"""
    file_path = os.path.join(
        os.path.dirname(__file__), "..", "dataset", f"{scenario}.json")
    json_data = read_json_file(file_path)

    if isinstance(json_data, str) and not json_data.startswith("Error"):
        result = select_two_random_nodes(json_data)
        
        if isinstance(result, tuple):
            node1, node2, belongs_to = result
            question = f"Does {node2} belong to {node1}?"
            if with_answer:
                answer = belongs_to
            else:
                answer = None
            return question, answer
    
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
 