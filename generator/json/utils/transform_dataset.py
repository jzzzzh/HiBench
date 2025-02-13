import json
import os
from pathlib import Path
import random

def load_dataset_structure(dataset_name):
    """Load the hierarchical structure JSON for a given dataset"""
    dataset_path = Path(__file__).parent.parent.parent.parent / "dataset" / "JSON" / "dataset" / f"{dataset_name}.json"
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset structure file not found: {dataset_path}")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_valid_qa_pair(qa_pair):
    """Check if a QA pair is valid (no None values and has required fields)"""
    return (qa_pair 
            and 'question' in qa_pair 
            and 'answer' in qa_pair 
            and qa_pair['question'] is not None 
            and qa_pair['answer'] is not None
            and qa_pair['question'].strip() != ''
            and qa_pair['answer'].strip() != '')

def transform_qa_data(input_dir, output_dir, items_per_scenario=5):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all question type directories
    question_types = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
    
    transformed_data = []
    datasets = ['university_structure_small', 'university_structure_medium_1', 
                'university_structure_medium_2', 'university_structure_large_1', 
                'university_structure_large_2']
    
    # Process each question type
    for q_type in question_types:
        # Process each dataset/scenario for this question type
        for dataset in datasets:
            try:
                # Load the hierarchical structure for this dataset
                dataset_structure = load_dataset_structure(dataset)
                dataset_structure_str = json.dumps(dataset_structure)
                
                # Load QA pairs for this question type and dataset
                file_path = os.path.join(input_dir, q_type, f"{q_type}_{dataset}.json")
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        qa_pairs = json.load(f)
                        
                        # Filter out invalid QA pairs
                        valid_qa_pairs = [qa for qa in qa_pairs if is_valid_qa_pair(qa)]
                        
                        if not valid_qa_pairs:
                            print(f"Warning: No valid QA pairs found in {file_path}")
                            continue
                        
                        # Select items_per_scenario questions from this file
                        selected_pairs = random.sample(valid_qa_pairs, min(len(valid_qa_pairs), items_per_scenario))
                        
                        # Add each selected pair to transformed data
                        for qa_pair in selected_pairs:
                            transformed_example = {
                                "instruction": f"As an AI agent, you are tasked with performing hierarchical structure reasoning to assist in understanding and analyzing complex organizational frameworks. Given the hierarchical structure {dataset_structure_str}, please answer question {qa_pair['question']}. Please return the answer in JSON format directly like {{\"answer\": \"{qa_pair['answer']}\" }} and do not feedback the detailed process.",
                                "input": "",
                                "output": "{\"answer\": \"" + qa_pair['answer'] + "\"}"
                            }
                            transformed_data.append(transformed_example)
            
            except Exception as e:
                print(f"Error processing {q_type} for dataset {dataset}: {str(e)}")
                continue
    
    # Write transformed data to output file
    output_file = os.path.join(output_dir, "transformed_dataset.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, indent=2, ensure_ascii=False)
    
    print(f"Transformed {len(transformed_data)} examples written to {output_file}")
    print(f"Expected number of examples: {len(question_types) * len(datasets) * items_per_scenario}")
    return output_file

if __name__ == "__main__":
    # Get the path to Test_dataset directory
    current_dir = Path(__file__).parent
    input_dir = current_dir.parent / "task_json" / "Test_dataset"
    output_dir = current_dir.parent / "task_json" / "transformed_dataset"
    
    transform_qa_data(str(input_dir), str(output_dir)) 