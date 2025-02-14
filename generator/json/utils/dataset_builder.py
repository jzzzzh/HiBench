import sys
import os
from tqdm import tqdm 
import json
import logging
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dataset_builder_debug.log'),
        logging.StreamHandler()
    ]
)

current_dir = os.path.dirname(os.path.abspath(__file__))  
project_root = os.path.dirname(current_dir)  
sys.path.append(project_root)

import qa.child_count as type_1
import qa.node_depth as type_2
import qa.level_count as type_3
import qa.node_attribute as type_5
import qa.level_nodes as type_6
import qa.path_down_to_up as type_7
import qa.path_up_to_down as type_8
import qa.shared_ancestor_same_level as type_9
import qa.shared_ancestor_diff_level as type_10
import qa.path_between_nodes as type_11

def generate_question_answer(scenario: str, question_type: int, with_answer: bool = True, layer_index: int = None):
    try:
        if question_type == 1:
            return type_1.gen_anwser_child_count(scenario=scenario, with_answer=with_answer, layer_index=layer_index, get_available_layers_func=get_available_layers)
        elif question_type == 2:
            return type_2.gen_anwser_node_depth(scenario=scenario, with_answer=with_answer, layer_index=layer_index, get_available_layers_func=get_available_layers)
        elif question_type == 3:
            return type_3.gen_anwser_level_count(scenario=scenario, with_answer=with_answer, layer_index=layer_index, get_available_layers_func=get_available_layers)
        elif question_type == 5:
            return type_5.gen_answer_node_attribute(scenario, with_answer=with_answer, get_available_layers_func=get_available_layers)
        elif question_type == 6:
            return type_6.gen_answer_level_nodes(scenario, with_answer=with_answer, get_available_layers_func=get_available_layers)
        elif question_type == 7:
            return type_7.gen_answer_path_down_to_up(scenario, with_answer=with_answer, get_available_layers_func=get_available_layers)
        elif question_type == 8:
            return type_8.gen_answer_path_up_to_down(scenario, with_answer=with_answer, get_available_layers_func=get_available_layers)
        elif question_type == 9:
            return type_9.gen_answer_shared_ancestor_same_level(scenario, with_answer=with_answer, get_available_layers_func=get_available_layers)
        elif question_type == 10:
            return type_10.gen_answer_shared_ancestor_diff_level(scenario, with_answer=with_answer, get_available_layers_func=get_available_layers)
        elif question_type == 11:
            return type_11.gen_answer_path_between_nodes(scenario, with_answer=with_answer, get_available_layers_func=get_available_layers)
        else:
            logging.error(f"Invalid question type: {question_type}")
            return None, None
    except Exception as e:
        logging.error(f"Error generating question type {question_type} for scenario {scenario}: {str(e)}")
        return None, None

def get_available_layers(scenario: str):
    """Get available layers for each scenario"""
    layers = {
        "university_structure_small": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_structure_medium_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_structure_medium_2": {
            "layers": [0, 1, 2,4],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_structure_large_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_structure_large_2": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        # Bullshit versions have same structure as their counterparts
        "university_bullshit_structure_small": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_bullshit_structure_medium_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_bullshit_structure_medium_2": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_bullshit_structure_large_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_bullshit_structure_large_2": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        }
    }
    
    if scenario not in layers:
        logging.error(f"No layer information found for scenario: {scenario}")
        return None
        
    logging.info(f"Found layers for {scenario}: {layers[scenario]}")
    return layers.get(scenario)

def is_duplicate_question(questions_answers: list, new_question: str) -> bool:
    """Check if a question already exists in the list"""
    return any(qa["question"] == new_question for qa in questions_answers)

def get_question_type_name(question_type: int) -> str:
    """Get descriptive name for question type"""
    type_names = {
        1: "child_count",
        2: "node_depth",
        3: "level_count",
        5: "node_attribute",
        6: "level_nodes",
        7: "path_down_to_up",
        8: "path_up_to_down",
        9: "shared_ancestor_same_level",
        10: "shared_ancestor_diff_level",
        11: "path_between_nodes"
    }
    return type_names.get(question_type, f"type_{question_type}")

def generate_test_data_set(scenario: str, with_answer: bool = True, number_of_questions: int = 40):
    """Generate test dataset based on scenario's available layers"""
    logging.info(f"Starting generation for scenario: {scenario}")
    
    # Update output paths for generated QA pairs
    base_path = os.path.join(
        os.path.dirname(__file__),  # generator/json/utils
        "..",                       # generator/json
        "task_json",                # generator/json/task_json
        "Test_dataset"              # generator/json/task_json/Test_dataset
    )
    
    # Get available layers for this scenario
    scenario_info = get_available_layers(scenario)
    if not scenario_info:
        error_msg = f"No layer information found for scenario: {scenario}"
        logging.error(error_msg)
        raise ValueError(error_msg)

    layers = scenario_info["layers"]
    valid_question_types = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    logging.debug(f"Available layers for {scenario}: {layers}")

    # Create base directory
    os.makedirs(base_path, exist_ok=True)
    logging.debug(f"Created output directory: {base_path}")

    # Total number of questions to generate
    total_operations = len(valid_question_types) * number_of_questions
    progress_bar = tqdm(total=total_operations, desc=f"Generating dataset for {scenario}")

    for question_type in valid_question_types:
        question_type_name = get_question_type_name(question_type)
        logging.info(f"Generating {question_type_name} questions for {scenario}")
        
        questions_answers = []
        duplicate_count = 0
        null_count = 0
        attempts = 0
        max_attempts = number_of_questions * 100  # Allow more attempts to get required questions

        while len(questions_answers) < number_of_questions and attempts < max_attempts:
            attempts += 1
            
            # Try to generate a valid, non-duplicate question
            question, answer = generate_question_answer(scenario, question_type, with_answer)
            
            if question is None or answer is None:
                null_count += 1
                logging.debug(f"Null attempt {null_count} for {question_type_name}")
                continue
                
            if not is_duplicate_question(questions_answers, question):
                questions_answers.append({"question": question, "answer": answer})
                progress_bar.update(1)
            else:
                duplicate_count += 1
                
        # Log statistics for this question type
        logging.info(f"Generated {len(questions_answers)} questions for {question_type_name}")
        logging.info(f"Duplicate attempts: {duplicate_count}")
        logging.info(f"Null attempts: {null_count}")
        logging.info(f"Total attempts: {attempts}")

        # Create question type directory and save results
        question_type_path = os.path.join(base_path, question_type_name)
        os.makedirs(question_type_path, exist_ok=True)
        
        file_name = os.path.join(question_type_path, f"{question_type_name}_{scenario}.json")
        
        if questions_answers:
            with open(file_name, "w") as file:
                json.dump(questions_answers, file, indent=4)
            logging.info(f"Successfully wrote {len(questions_answers)} questions to {file_name}")
        else:
            logging.warning(f"No questions generated for type {question_type}, scenario {scenario}")

    progress_bar.close()
    logging.debug(f"Completed dataset generation for scenario: {scenario}")

def verify_dataset_alignment(scenarios):
    """Verify that normal and bullshit datasets have matching structures"""
    logging.info("Verifying dataset alignment...")
    
    # Get absolute path to project root (HiBench directory)
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
    
    logging.info(f"Project root path: {project_root}")

    # Update scenario pairs to match actual file names
    scenario_pairs = {
        'structure_medium_1': {
            'normal': 'university_structure_medium_1',
            'bullshit': 'university_bullshit_structure_medium_1'
        },
        'structure_medium_2': {
            'normal': 'university_structure_medium_2',
            'bullshit': 'university_bullshit_structure_medium_2'
        },
        'structure_large_1': {
            'normal': 'university_structure_large_1',
            'bullshit': 'university_bullshit_structure_large_1'
        },
        'structure_large_2': {
            'normal': 'university_structure_large_2',
            'bullshit': 'university_bullshit_structure_large_2'
        },
        'structure_small': {
            'normal': 'university_structure_small',
            'bullshit': 'university_bullshit_structure_small'
        }
    }

    alignment_report = {}
    is_aligned = True

    for base_name, pair in scenario_pairs.items():
        # Construct absolute paths
        normal_path = os.path.join(
            project_root,
            "dataset",
            "JSON",
            "dataset",
            f"{pair['normal']}.json"
        )
        bullshit_path = os.path.join(
            project_root,
            "dataset",
            "JSON",
            "dataset",
            f"{pair['bullshit']}.json"
        )

        logging.info(f"Checking normal file: {normal_path}")
        logging.info(f"Checking bullshit file: {bullshit_path}")

        # Verify file existence before trying to open
        if not os.path.exists(normal_path):
            error_msg = f"Normal file not found: {normal_path}"
            logging.error(error_msg)
            alignment_report[base_name] = {
                'normal_file': pair['normal'],
                'bullshit_file': pair['bullshit'],
                'error': error_msg
            }
            is_aligned = False
            continue

        if not os.path.exists(bullshit_path):
            error_msg = f"Bullshit file not found: {bullshit_path}"
            logging.error(error_msg)
            alignment_report[base_name] = {
                'normal_file': pair['normal'],
                'bullshit_file': pair['bullshit'],
                'error': error_msg
            }
            is_aligned = False
            continue

        try:
            with open(normal_path, 'r', encoding='utf-8') as f:
                normal_data = json.load(f)
            with open(bullshit_path, 'r', encoding='utf-8') as f:
                bullshit_data = json.load(f)

            # Compare structure lengths
            normal_length = len(normal_data)
            bullshit_length = len(bullshit_data)
            
            alignment_report[base_name] = {
                'normal_file': pair['normal'],
                'bullshit_file': pair['bullshit'],
                'normal_length': normal_length,
                'bullshit_length': bullshit_length,
                'is_aligned': normal_length == bullshit_length,
                'error': None
            }

            if normal_length != bullshit_length:
                is_aligned = False
                error_msg = f"Length mismatch: normal={normal_length}, bullshit={bullshit_length}"
                alignment_report[base_name]['error'] = error_msg
                logging.error(f"Dataset alignment error for {base_name}: {error_msg}")

        except Exception as e:
            is_aligned = False
            error_msg = f"Error comparing datasets: {str(e)}"
            alignment_report[base_name] = {
                'normal_file': pair['normal'],
                'bullshit_file': pair['bullshit'],
                'error': error_msg
            }
            logging.error(f"Dataset verification error for {base_name}: {error_msg}")

    return is_aligned, alignment_report

def generate_dataset_report():
    """Generate a Markdown report describing the dataset demographics"""
    report_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "task_json",
        "reports"
    )
    report_path = os.path.join(report_dir, "DATASET_REPORT.md")
    
    # Ensure directories exist
    os.makedirs(report_dir, exist_ok=True)
    
    # Initialize statistics dictionary
    stats = {
        "total_questions": 0,
        "by_question_type": defaultdict(int),
        "by_scenario": defaultdict(int),
        "detailed_stats": defaultdict(lambda: defaultdict(int))  # scenario -> question_type -> count
    }
    
    # Get test dataset directory
    test_dataset_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "task_json",
        "Test_dataset"
    )

    # Collect statistics
    question_types = [
        'child_count', 'node_depth', 'level_count',
        'node_attribute', 'level_nodes', 'path_down_to_up', 'path_up_to_down',
        'shared_ancestor_same_level', 'shared_ancestor_diff_level', 'path_between_nodes'
    ]

    # Generate Markdown report
    with open(report_path, 'w') as f:
        f.write("# Dataset Demographics Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Collect and write detailed statistics
        f.write("## Detailed Statistics by Question Type and Scenario\n\n")
        f.write("| Question Type | Scenario | Number of Questions |\n")
        f.write("|--------------|----------|-------------------|\n")

        for question_type in question_types:
            question_type_dir = os.path.join(test_dataset_dir, question_type)
            if not os.path.exists(question_type_dir):
                continue

            for file_name in os.listdir(question_type_dir):
                if not file_name.endswith('.json'):
                    continue

                file_path = os.path.join(question_type_dir, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        questions = json.load(json_file)
                        num_questions = len(questions)
                        
                        # Extract scenario name from file name
                        scenario = file_name.replace(f"{question_type}_", "").replace(".json", "")
                        
                        # Update statistics
                        stats["total_questions"] += num_questions
                        stats["by_question_type"][question_type] += num_questions
                        stats["by_scenario"][scenario] += num_questions
                        stats["detailed_stats"][scenario][question_type] = num_questions
                        
                        # Write to report
                        f.write(f"| {question_type} | {scenario} | {num_questions} |\n")
                except Exception as e:
                    logging.error(f"Error processing file {file_path}: {str(e)}")

        # Write summary statistics
        f.write("\n## Summary Statistics\n\n")
        f.write(f"Total number of questions: {stats['total_questions']}\n\n")

        # Questions by scenario
        f.write("### Questions by Scenario\n\n")
        f.write("| Scenario | Total Questions |\n")
        f.write("|----------|----------------|\n")
        for scenario, count in sorted(stats["by_scenario"].items()):
            f.write(f"| {scenario} | {count} |\n")

        # Questions by type
        f.write("\n### Questions by Type\n\n")
        f.write("| Question Type | Total Questions |\n")
        f.write("|--------------|----------------|\n")
        for qtype, count in sorted(stats["by_question_type"].items()):
            f.write(f"| {qtype} | {count} |\n")

    logging.info(f"Dataset report generated: {report_path}")

def ensure_directory_structure():
    """Ensure all required directories exist"""
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
    
    required_dirs = [
        os.path.join(project_root, "dataset", "JSON", "dataset"),
        os.path.join(project_root, "generator", "json", "task_json", "Test_dataset"),
        os.path.join(project_root, "generator", "json", "task_json", "reports")
    ]

    for directory in required_dirs:
        if not os.path.exists(directory):
            logging.info(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)

    return project_root

if __name__ == "__main__":
    logging.info("Starting dataset generation process")
    
    # Ensure directory structure exists
    project_root = ensure_directory_structure()
    logging.info(f"Project root: {project_root}")
    
    # First verify dataset alignment
    is_aligned, alignment_report = verify_dataset_alignment([])
    if not is_aligned:
        logging.error("Dataset alignment check failed. See report for details.")
        logging.error("Alignment report:")
        for base_name, info in alignment_report.items():
            if info.get('error'):
                logging.error(f"{base_name}: {info['error']}")
        sys.exit(1)

    logging.info("Dataset alignment check passed. Proceeding with generation...")

    # Update scenario question counts to match actual file names
    scenario_question_counts = {
        "university_structure_medium_1": 13,
        "university_bullshit_structure_medium_1": 13,
        "university_structure_medium_2": 13,
        "university_bullshit_structure_medium_2": 13,
        "university_structure_large_1": 13,
        "university_bullshit_structure_large_1": 13,
        "university_structure_large_2": 13,
        "university_bullshit_structure_large_2": 13,
        "university_structure_small": 13,
        "university_bullshit_structure_small": 13
    }

    # Generate datasets for each scenario
    scenarios = list(scenario_question_counts.keys())
    for scenario in scenarios:
        question_count = scenario_question_counts[scenario]
        generate_test_data_set(scenario, True, question_count)
    
    # Generate report after creating all datasets
    generate_dataset_report()
    logging.info("Completed all dataset generation")