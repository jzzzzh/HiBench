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
import qa.node_relationship as type_4
import qa.node_attribute as type_5
import qa.level_nodes as type_6
import qa.path_down_to_up as type_7
import qa.path_up_to_down as type_8
import qa.shared_ancestor_same_level as type_9
import qa.shared_ancestor_diff_level as type_10
import qa.path_between_nodes as type_11

def generate_question_answer(scenario: str, question_type: int, with_answer: bool = True, layer_index: int = None):
    if question_type == 1:
        return type_1.gen_anwser_child_count(scenario=scenario, with_answer=with_answer, layer_index=layer_index)
    elif question_type == 2:
        return type_2.gen_anwser_node_depth(scenario=scenario, with_answer=with_answer, layer_index=layer_index)
    elif question_type == 3:
        return type_3.gen_anwser_level_count(scenario=scenario, with_answer=with_answer, layer_index=layer_index)
    elif question_type == 4:
        return type_4.gen_answer_node_relationship(scenario, with_answer=with_answer)
    elif question_type == 5:
        return type_5.gen_answer_node_attribute(scenario, with_answer=with_answer)
    elif question_type == 6:
        return type_6.gen_answer_level_nodes(scenario, with_answer=with_answer)
    elif question_type == 7:
        return type_7.gen_answer_path_down_to_up(scenario, with_answer=with_answer)
    elif question_type == 8:
        return type_8.gen_answer_path_up_to_down(scenario, with_answer=with_answer)
    elif question_type == 9:
        return type_9.gen_answer_shared_ancestor_same_level(scenario, with_answer=with_answer)
    elif question_type == 10:
        return type_10.gen_answer_shared_ancestor_diff_level(scenario, with_answer=with_answer)
    elif question_type == 11:
        return type_11.gen_answer_path_between_nodes(scenario, with_answer=with_answer)
    else:
        raise ValueError("Invalid question type")

def get_available_layers(scenario: str):
    """Get available layers for each scenario"""
    layers = {
        "university_structure_small": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_structure_medium_01": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_structure_medium_02": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_structure_large_01": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_structure_large_02": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        # Bullshit versions have same structure as their counterparts
        "university_bullshit_structure_small": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_bullshit_structure_medium_01": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_bullshit_structure_medium_02": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_bullshit_structure_large_01": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_bullshit_structure_large_02": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        }
    }
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
        4: "node_relationship",
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
    # Get the absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    base_path = os.path.join(project_root, "task_json", "Test_dataset")
    
    logging.debug(f"Starting dataset generation for scenario: {scenario}")
    valid_scenarios = [
        "university_structure_small",
        "university_structure_medium_01",
        "university_structure_medium_02",
        "university_structure_large_01",
        "university_structure_large_02",
        "university_bullshit_structure_small",
        "university_bullshit_structure_medium_01",
        "university_bullshit_structure_medium_02",
        "university_bullshit_structure_large_01",
        "university_bullshit_structure_large_02"
    ]
    
    if scenario not in valid_scenarios:
        error_msg = f"Invalid scenario name: {scenario}"
        logging.error(error_msg)
        raise ValueError(error_msg)

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

    MAX_DUPLICATE_TRIES = 50  # Maximum attempts to generate a non-duplicate question
    MAX_NULL_TRIES = 50       # Maximum attempts to generate a non-null question

    for question_type in valid_question_types:
        logging.debug(f"Processing question type: {question_type}")
        # Create question type directory using descriptive name
        question_type_name = get_question_type_name(question_type)
        question_type_path = os.path.join(base_path, question_type_name)
        os.makedirs(question_type_path, exist_ok=True)
        logging.debug(f"Created question type directory: {question_type_path}")

        # Create file path with descriptive name
        file_name = os.path.join(question_type_path, f"{question_type_name}_{scenario}.json")
        logging.debug(f"Will save to file: {file_name}")
        questions_answers = []
        
        # For layer-specific questions (types 1-3)
        if question_type in [1, 2, 3]:
            logging.debug(f"Processing layer-specific questions for type {question_type}")
            questions_per_layer = number_of_questions // len(layers)
            for layer_index in layers:
                logging.debug(f"Processing layer {layer_index}")
                generated_count = 0
                duplicate_tries = 0
                null_tries = 0
                
                while (generated_count < questions_per_layer and 
                       duplicate_tries < MAX_DUPLICATE_TRIES and
                       null_tries < MAX_NULL_TRIES):
                    question, answer = generate_question_answer(
                        scenario=scenario,
                        question_type=question_type,
                        with_answer=with_answer,
                        layer_index=layer_index
                    )
                    
                    # Skip if question or answer is None
                    if question is None or answer is None:
                        warning_msg = f"Skipping null question-answer pair for type {question_type}, layer {layer_index}"
                        logging.warning(warning_msg)
                        null_tries += 1
                        continue
                    
                    # Skip if question is duplicate
                    if is_duplicate_question(questions_answers, question):
                        logging.debug(f"Skipping duplicate question: {question[:50]}...")
                        duplicate_tries += 1
                        continue
                        
                    questions_answers.append({
                        "question": question,
                        "answer": answer
                    })
                    generated_count += 1
                    duplicate_tries = 0
                    null_tries = 0
                
                if duplicate_tries >= MAX_DUPLICATE_TRIES or null_tries >= MAX_NULL_TRIES:
                    logging.warning(f"Reached maximum tries for type {question_type}, layer {layer_index}. "
                                  f"Generated {generated_count}/{questions_per_layer} questions.")
                    # Write what we have so far
                    if generated_count > 0:
                        progress_bar.update(questions_per_layer - generated_count)  # Update progress bar for skipped questions
            
            # For remaining questions
            remaining_questions = number_of_questions % len(layers)
            if remaining_questions > 0:
                generated_count = 0
                duplicate_tries = 0
                null_tries = 0
                
                while (generated_count < remaining_questions and 
                       duplicate_tries and
                       null_tries < MAX_NULL_TRIES):
                    question, answer = generate_question_answer(
                        scenario=scenario,
                        question_type=question_type,
                        with_answer=with_answer,
                        layer_index=layers[0]
                    )
                    
                    # Skip if question or answer is None
                    if question is None or answer is None:
                        warning_msg = f"Skipping null question-answer pair for type {question_type}, layer {layers[0]}"
                        logging.warning(warning_msg)
                        null_tries += 1
                        continue
                    
                    # Skip if question is duplicate
                    if is_duplicate_question(questions_answers, question):
                        logging.debug(f"Skipping duplicate question: {question[:50]}...")
                        duplicate_tries += 1
                        continue
                        
                    questions_answers.append({
                        "question": question,
                        "answer": answer
                    })
                    generated_count += 1
                    duplicate_tries = 0
                    null_tries = 0
                
                if duplicate_tries >= MAX_DUPLICATE_TRIES or null_tries >= MAX_NULL_TRIES:
                    logging.warning(f"Reached maximum tries for remaining questions of type {question_type}. "
                                  f"Generated {generated_count}/{remaining_questions} questions.")
                    if generated_count > 0:
                        progress_bar.update(remaining_questions - generated_count)
        
        # For non-layer-specific questions (types 4-11)
        else:
            logging.debug(f"Processing non-layer-specific questions for type {question_type}")
            generated_count = 0
            true_count = 0
            false_count = 0
            target_true = number_of_questions // 2
            target_false = number_of_questions - target_true
            duplicate_tries = 0
            null_tries = 0
            
            while (generated_count < number_of_questions and 
                   duplicate_tries < MAX_DUPLICATE_TRIES and
                   null_tries < MAX_NULL_TRIES):
                question, answer = generate_question_answer(
                    scenario=scenario,
                    question_type=question_type,
                    with_answer=with_answer
                )
                
                # Skip if question or answer is None
                if question is None or answer is None:
                    warning_msg = f"Skipping null question-answer pair for type {question_type}"
                    logging.warning(warning_msg)
                    null_tries += 1
                    continue
                
                # Skip if question is duplicate
                if is_duplicate_question(questions_answers, question):
                    logging.debug(f"Skipping duplicate question: {question[:50]}...")
                    duplicate_tries += 1
                    continue
                
                # For type 4, ensure balanced True/False answers
                if question_type == 4:
                    if answer is True and true_count < target_true:
                        questions_answers.append({"question": question, "answer": answer})
                        true_count += 1
                        generated_count += 1
                        duplicate_tries = 0
                        null_tries = 0
                        progress_bar.update(1)
                        logging.debug(f"Added True answer. Current True count: {true_count}/{target_true}")
                    elif answer is False and false_count < target_false:
                        questions_answers.append({"question": question, "answer": answer})
                        false_count += 1
                        generated_count += 1
                        duplicate_tries = 0
                        null_tries = 0
                        progress_bar.update(1)
                        logging.debug(f"Added False answer. Current False count: {false_count}/{target_false}")
                    # If we get an answer we don't need, just continue trying
                    continue
                else:
                    questions_answers.append({"question": question, "answer": answer})
                    generated_count += 1
                    duplicate_tries = 0
                    null_tries = 0
                    progress_bar.update(1)
            
            if duplicate_tries >= MAX_DUPLICATE_TRIES or null_tries >= MAX_NULL_TRIES:
                logging.warning(f"Reached maximum tries for type {question_type}. "
                              f"Generated {generated_count}/{number_of_questions} questions. "
                              f"True/False ratio - True: {true_count}/{target_true}, False: {false_count}/{target_false}")
                if generated_count > 0:
                    progress_bar.update(number_of_questions - generated_count)
        
        # Write all questions to a single file, even if incomplete
        if questions_answers:  # Only write if we have some questions
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            
            logging.debug(f"Writing {len(questions_answers)} questions to {file_name}")
            with open(file_name, "w") as file:
                json.dump(questions_answers, file, indent=4)
            logging.debug(f"Successfully wrote file: {file_name}")
        else:
            logging.warning(f"No questions generated for type {question_type}, scenario {scenario}")

    progress_bar.close()
    logging.debug(f"Completed dataset generation for scenario: {scenario}")

def generate_dataset_report():
    """Generate a Markdown report describing the dataset demographics"""
    # Get the absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    base_path = os.path.join(project_root, "task_json", "Test_dataset")  # Changed path to include task_json
    report_dir = os.path.join(project_root, "task_json", "reports")      # Changed path to include task_json
    report_path = os.path.join(report_dir, "DATASET_REPORT.md")
    
    # Ensure directories exist
    os.makedirs(base_path, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    
    stats = {
        "total_questions": 0,
        "by_question_type": defaultdict(int),
        "by_scenario": defaultdict(int),
        "type_4_true_false": {"true": 0, "false": 0},
        "questions_per_file": defaultdict(list)
    }
    
    # Collect statistics
    for question_type in range(1, 12):
        type_dir = os.path.join(base_path, get_question_type_name(question_type))
        if not os.path.exists(type_dir):
            continue
            
        for file_name in os.listdir(type_dir):
            if not file_name.endswith('.json'):
                continue
                
            file_path = os.path.join(type_dir, file_name)
            scenario = file_name.split('_')[-1].replace('.json', '')
            
            with open(file_path, 'r') as f:
                questions = json.load(f)
                
                stats["questions_per_file"][file_name] = len(questions)
                stats["total_questions"] += len(questions)
                stats["by_question_type"][question_type] += len(questions)
                stats["by_scenario"][scenario] += len(questions)
                
                # Special handling for Type 4 (True/False distribution)
                if question_type == 4:
                    for qa in questions:
                        if qa["answer"]:
                            stats["type_4_true_false"]["true"] += 1
                        else:
                            stats["type_4_true_false"]["false"] += 1

    # Generate Markdown report
    with open(report_path, 'w') as f:
        f.write("# Dataset Demographics Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Overall statistics
        f.write("## Overall Statistics\n\n")
        f.write(f"- Total number of questions: {stats['total_questions']}\n")
        f.write(f"- Number of question types: {len(stats['by_question_type'])}\n")
        f.write(f"- Number of scenarios: {len(stats['by_scenario'])}\n\n")
        
        # Question type distribution
        f.write("## Distribution by Question Type\n\n")
        f.write("| Question Type | Number of Questions |\n")
        f.write("|--------------|-------------------|\n")
        for qtype, count in sorted(stats["by_question_type"].items()):
            f.write(f"| Type {qtype} | {count} |\n")
        f.write("\n")
        
        # Scenario distribution
        f.write("## Distribution by Scenario\n\n")
        f.write("| Scenario | Number of Questions |\n")
        f.write("|----------|-------------------|\n")
        for scenario, count in sorted(stats["by_scenario"].items()):
            f.write(f"| {scenario} | {count} |\n")
        f.write("\n")
        
        # Type 4 True/False distribution
        f.write("## Type 4 (True/False) Distribution\n\n")
        total_type4 = stats["type_4_true_false"]["true"] + stats["type_4_true_false"]["false"]
        if total_type4 > 0:
            true_percent = (stats["type_4_true_false"]["true"] / total_type4) * 100
            false_percent = (stats["type_4_true_false"]["false"] / total_type4) * 100
            f.write(f"- True answers: {stats['type_4_true_false']['true']} ({true_percent:.1f}%)\n")
            f.write(f"- False answers: {stats['type_4_true_false']['false']} ({false_percent:.1f}%)\n\n")
        
        # Detailed file statistics
        f.write("## Questions per File\n\n")
        f.write("| File Name | Number of Questions |\n")
        f.write("|-----------|-------------------|\n")
        for file_name, count in sorted(stats["questions_per_file"].items()):
            f.write(f"| {file_name} | {count} |\n")

    logging.info(f"Dataset report generated: {report_path}")

if __name__ == "__main__":
    logging.info("Starting dataset generation process")
    # List of all scenarios
    scenarios = [
        "university_structure_small",
        "university_structure_medium_01",
        "university_structure_medium_02",
        "university_structure_large_01",
        "university_structure_large_02",
        "university_bullshit_structure_small",
        "university_bullshit_structure_medium_01",
        "university_bullshit_structure_medium_02",
        "university_bullshit_structure_large_01",
        "university_bullshit_structure_large_02"
    ]
    #generate_test_data_set("university_bullshit_structure_medium_02", True)
    # Generate datasets for each scenario
    for scenario in scenarios:
        generate_test_data_set(scenario, True)
    
    # Generate report after creating all datasets
    generate_dataset_report()
    logging.info("Completed all dataset generation")

"""
Layer Structure for University Scenarios:

university_structure_small:
- Layers: 3
- Structure:
  0: Faculty
  1: Department
  2: Program

university_structure_medium_01:
- Layers: 6
- Structure:
  0: Faculty
  1: Department
  2: Program
  3: Course
  4: Lecturer
  5: Student

university_structure_medium_02:
- Layers: 3
- Structure:
  0: Faculty
  1: Department
  2: Program

university_structure_large_01:
- Layers: 6
- Structure:
  0: Faculty
  1: Department
  2: Program
  3: Course
  4: Lecturer
  5: Student

university_structure_large_02:
- Layers: 3
- Structure:
  0: Faculty
  1: Department
  2: Program
"""