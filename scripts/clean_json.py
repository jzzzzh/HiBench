import os
import re
import json
import logging

def pluralize_content(text):
    """Replace singular forms with plural forms in the given text."""
    replacements = {
        "Faculty": "Faculties",
        "Department": "Departments",
        "Program": "Programs",
        "Course": "Courses",
        "Lecturer": "Lecturers",
        "Student": "Students"
    }
    
    # Split text into words
    words = text.split()
    
    # Process each word
    for i, word in enumerate(words):
        # Check if the word exactly matches any of our singular forms
        for singular, plural in replacements.items():
            if word == singular:
                words[i] = plural
                break
            # Handle case where word starts with singular form (e.g., "Department of...")
            elif word.startswith(singular) and not word.endswith('s'):
                words[i] = word.replace(singular, plural, 1)
                break
    
    # Rejoin the words
    return ' '.join(words)
def normalize_question(question):
    """Normalize question by removing period, standardizing pluralization and whitespace"""
    # Remove trailing period and whitespace
    question = question.rstrip('.').strip()
    
    # Standardize pluralization
    question = pluralize_content(question)
    
    return question
def check_question_matching_Results(qa_path, results_path):
    """Check if all questions in results have matches in QA dataset"""
    logger = logging.getLogger()
    all_matched = True
    
    # Read QA dataset
    qa_data = {}
    for filename in os.listdir(qa_path):
        if filename.endswith('.json'):
            qa_file_path = os.path.join(qa_path, filename)
            with open(qa_file_path, 'r', encoding='utf-8') as f:
                try:
                    qa_json = json.load(f)
                    for item in qa_json:
                        if "question" in item:
                            normalized_question = normalize_question(item["question"])
                            qa_data[normalized_question] = item["answer"]
                except json.JSONDecodeError as e:
                    logger.error(f"Error reading QA file {qa_file_path}: {e}")
                    return False

    # Check results files
    for filename in os.listdir(results_path):
        if filename.endswith('.json'):
            results_file_path = os.path.join(results_path, filename)
            with open(results_file_path, 'r', encoding='utf-8') as f:
                try:
                    results_json = json.load(f)
                    for item in results_json:
                        if "UserPrompt" in item:
                            question = parse_question_from_user_prompt(item["UserPrompt"])
                            if question:
                                normalized_question = normalize_question(question)
                                if normalized_question not in qa_data:
                                    if all_matched:
                                        logger.error(f"Unmatched questions found in {filename}:")
                                    logger.error(f"  - Original Question: {question}")
                                    logger.error(f"  - Normalized Question: {normalized_question}")
                                    logger.error(f"  - Available QA questions: {list(qa_data.keys())}")
                                    all_matched = False
                except json.JSONDecodeError as e:
                    logger.error(f"Error reading results file {results_file_path}: {e}")
                    return False

    return all_matched
def extract_dataset_key(filename):
    """Extract dataset key from filename"""
    pattern = r"(university(?:_bullshit)?_structure_[^\.]+)"
    match = re.search(pattern, filename)
    if not match:
        return None
    
    entire = match.group(1)
    short_pattern = r"(university(?:_bullshit)?_structure_[a-zA-Z0-9]+)"
    short_match = re.search(short_pattern, entire)
    return short_match.group(1) if short_match else entire

def parse_question_from_user_prompt(user_prompt):
    """Extract the question from UserPrompt"""
    if "List " not in user_prompt:
        return user_prompt
        
    start_marker = "List "
    end_marker = "..\n"

    start_index = user_prompt.find(start_marker)
    if start_index == -1:
        return None

    end_index = user_prompt.find(end_marker, start_index)
    if end_index == -1:
        end_index = user_prompt.find(".", start_index)

    if end_index == -1:
        end_index = len(user_prompt)

    return user_prompt[start_index:end_index].strip()


def load_folder_a_data(folder_a):
    """Load data from folder A: dataset_key -> (question -> answer)"""
    a_data = {}
    
    for filename in os.listdir(folder_a):
        if not filename.endswith(".json"):
            continue
            
        file_path = os.path.join(folder_a, filename)
        dataset_key = extract_dataset_key(filename)
        if not dataset_key:
            continue
            
        if dataset_key not in a_data:
            a_data[dataset_key] = {}
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                a_json = json.load(f)
                for item in a_json:
                    if "question" in item and "answer" in item:
                        a_data[dataset_key][item["question"]] = item["answer"]
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON in file '{file_path}': {e}")
            continue
            
    return a_data

def update_results(qa_path, results_path, output_path):
    """Update TrueAnswer in results with answers from QA dataset"""
    logger = logging.getLogger()
    
    # First check if all questions match
    if not check_question_matching_Results(qa_path, results_path):
        logger.error("Question matching check failed. Stopping update process.")
        return False
        
    logger.info("All questions matched. Proceeding with updates...")
    
    # Create output folder
    os.makedirs(output_path, exist_ok=True)
    
    # Read QA dataset
    qa_data = {}
    for filename in os.listdir(qa_path):
        if filename.endswith('.json'):
            with open(os.path.join(qa_path, filename), 'r', encoding='utf-8') as f:
                qa_json = json.load(f)
                for item in qa_json:
                    if "question" in item:
                        normalized_question = normalize_question(item["question"])
                        qa_data[normalized_question] = item["answer"]

    # Update results files
    for filename in os.listdir(results_path):
        if filename.endswith('.json'):
            input_file = os.path.join(results_path, filename)
            output_file = os.path.join(output_path, filename)
            
            with open(input_file, 'r', encoding='utf-8') as f:
                results_json = json.load(f)
                
                # Update each result
                for item in results_json:
                    if "UserPrompt" in item:
                        question = parse_question_from_user_prompt(item["UserPrompt"])
                        if question:
                            normalized_question = normalize_question(question)
                            if normalized_question in qa_data:
                                item["TrueAnswer"] = qa_data[normalized_question]

            # Save updated results
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results_json, f, indent=4, ensure_ascii=False)
            logger.info(f"Updated file saved: {output_file}")
    
    return True


def check_question_matching(folder_a, folder_b):
    """Check if all questions in folder_a (dataset) have matches in folder_b (correct_QA)"""
    logger = logging.getLogger()
    all_matched = True
    
    # Read data from folder B (correct_QA) into a dictionary keyed by filename
    b_data = {}
    for filename in os.listdir(folder_b):
        if filename.endswith('.json'):
            b_file_path = os.path.join(folder_b, filename)
            with open(b_file_path, 'r', encoding='utf-8') as f_b:
                try:
                    b_data[filename] = json.load(f_b)
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON in file {b_file_path}: {e}")
                    return False

    # Check each JSON file in folder A (dataset)
    for filename in os.listdir(folder_a):
        if filename.endswith('.json'):
            a_file_path = os.path.join(folder_a, filename)
            with open(a_file_path, 'r', encoding='utf-8') as f_a:
                try:
                    a_json = json.load(f_a)
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON in file {a_file_path}: {e}")
                    return False

            if filename not in b_data:
                logger.error(f"Missing corresponding file in correct_QA: {filename}")
                return False

            b_json = b_data[filename]
            b_questions = {item.get("question") for item in b_json if item.get("question")}
            
            # Check if each question in A has a match in B
            for item_a in a_json:
                a_question = item_a.get("question")
                if a_question and a_question not in b_questions:
                    if all_matched:  # Only print header for first error
                        logger.error(f"Unmatched questions found in {filename}:")
                    logger.error(f"  - {a_question}")
                    all_matched = False

    return all_matched

def correct_answers_QA_dataset(folder_a, folder_b, output_folder):
    """Replace answers only if all questions match"""
    logger = logging.getLogger()
    
    # First check if all questions match
    
    if not check_question_matching(folder_a, folder_b):
        logger.error("Question matching check failed. Stopping replacement process.")
        return False
        
    # If all questions match, proceed with replacement
    logger.info("All questions matched. Proceeding with answer replacement...")
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Read folder B data
    b_data = {}
    for filename in os.listdir(folder_b):
        if filename.endswith('.json'):
            with open(os.path.join(folder_b, filename), 'r', encoding='utf-8') as f_b:
                b_data[filename] = json.load(f_b)

    # Process each file in folder A
    for filename in os.listdir(folder_a):
        if filename.endswith('.json'):
            a_file_path = os.path.join(folder_a, filename)
            with open(a_file_path, 'r', encoding='utf-8') as f_a:
                a_json = json.load(f_a)

            # Replace answers
            for item_a in a_json:
                a_question = item_a.get("question")
                for item_b in b_data[filename]:
                    if item_b.get("question") == a_question:
                        item_a["answer"] = item_b.get("answer", "")
                        break

            # Save corrected file
            output_path = os.path.join(output_folder, filename)
            with open(output_path, 'w', encoding='utf-8') as out_f:
                json.dump(a_json, out_f, indent=4, ensure_ascii=False)
            logger.info(f"Corrected file saved: {output_path}")
    
    return True
def process_nested_folders(qa_path, results_base_path, output_base_path):
    """Process all nested folders containing JSON files"""
    logger = logging.getLogger()
    
    # Read QA dataset once
    qa_data = {}
    for filename in os.listdir(qa_path):
        if filename.endswith('.json'):
            with open(os.path.join(qa_path, filename), 'r', encoding='utf-8') as f:
                qa_json = json.load(f)
                for item in qa_json:
                    if "question" in item:
                        normalized_question = normalize_question(item["question"])
                        qa_data[normalized_question] = item["answer"]

    def process_directory(current_path, relative_path=""):
        """Recursively process directories and update JSON files"""
        current_output_path = os.path.join(output_base_path, relative_path)
        os.makedirs(current_output_path, exist_ok=True)
        
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            relative_item_path = os.path.join(relative_path, item)
            
            if os.path.isdir(item_path):
                # Recursively process subdirectories
                process_directory(item_path, relative_item_path)
            elif item.endswith('.json'):
                # Process JSON file
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        results_json = json.load(f)
                    
                    # Update each result
                    for result_item in results_json:
                        if "UserPrompt" in result_item:
                            question = parse_question_from_user_prompt(result_item["UserPrompt"])
                            if question:
                                normalized_question = normalize_question(question)
                                if normalized_question in qa_data:
                                    result_item["TrueAnswer"] = qa_data[normalized_question]
                                else:
                                    logger.warning(f"No match found for question in {item_path}: {question}")
                    
                    # Save updated file
                    output_file_path = os.path.join(current_output_path, item)
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        json.dump(results_json, f, indent=4, ensure_ascii=False)
                    logger.info(f"Updated file saved: {output_file_path}")
                    
                except Exception as e:
                    logger.error(f"Error processing file {item_path}: {str(e)}")

    # Start processing from the base results path
    process_directory(results_base_path)
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('update_true_answers.log'),
            logging.StreamHandler()
        ]
        )
    corrected_QA_dataset_path = "/Users/youngj/Local/Project/HiBench/dataset/JSON/QA/level_nodes"
    results_base_path = "/Users/youngj/Downloads/Results_3/JSON/level_nodes"
    output_base_path = "/Users/youngj/Downloads/Results_3/JSON/updated_level_nodes"
    process_nested_folders(corrected_QA_dataset_path, results_base_path, output_base_path)

    #correct_answers_QA_dataset(dataset_file_path, correct_QA, corrected_QA_dataset_path)

    #update_results(corrected_QA_dataset_path, result_file_path, output_results_folder_path)
