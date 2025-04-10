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
    
    # Convert text to lowercase for comparison
    text_lower = text.lower()
    result_words = []
    
    for word in text.split():
        word_lower = word.lower()
        replaced = False
        
        for singular, plural in replacements.items():
            if word_lower == singular.lower() or word_lower == plural.lower():
                result_words.append(plural)
                replaced = True
                break
        
        if not replaced:
            result_words.append(word)
    
    return ' '.join(result_words)
def debug_question_matching(qa_path, results_path):
    """Debug function to print normalized questions and their matches"""
    # Read QA dataset
    qa_data = {}
    print("\nQA Dataset Questions:")
    for filename in os.listdir(qa_path):
        if filename.endswith('.json'):
            with open(os.path.join(qa_path, filename), 'r', encoding='utf-8') as f:
                qa_json = json.load(f)
                for item in qa_json:
                    if "question" in item:
                        orig_question = item["question"]
                        norm_question = normalize_question(orig_question)
                        print(f"Original: {orig_question}")
                        print(f"Normalized: {norm_question}")
                        print(f"Answer: {item['answer']}\n")
                        qa_data[norm_question] = item["answer"]

    print("\nResults File Questions:")
    for filename in os.listdir(results_path):
        if filename.endswith('.json'):
            with open(os.path.join(results_path, filename), 'r', encoding='utf-8') as f:
                results_json = json.load(f)
                for item in results_json:
                    if "UserPrompt" in item:
                        question = parse_question_from_user_prompt(item["UserPrompt"])
                        if question:
                            norm_question = normalize_question(question)
                            print(f"Original: {question}")
                            print(f"Normalized: {norm_question}")
                            print(f"Found in QA: {norm_question in qa_data}")
                            if norm_question in qa_data:
                                print(f"QA Answer: {qa_data[norm_question]}\n")
def normalize_question(question):
    """Normalize question by removing period, standardizing pluralization and whitespace"""
    # Remove trailing period and whitespace
    question = question.rstrip('.').strip()
    
    # Convert to lowercase for consistent matching
    question = question.lower()
    
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
def extract_dataset_info(filename):
    """
    Extract both the task type and dataset name from a filename.
    Returns: tuple(task_type, dataset_name) or None if no match
    """
    # First try to match the task filename pattern
    task_pattern = r"Task_JSON_SubTask_(level_(?:count|nodes))_Domain_(university(?:_bullshit)?_structure_(?:small|medium|large)(?:_\d+)?)"
    match = re.search(task_pattern, filename)
    if match:
        return (match.group(1), match.group(2))
        
    # If not a task file, try to match the QA dataset pattern
    qa_pattern = r"(level_(?:count|nodes))_(university(?:_bullshit)?_structure_(?:small|medium|large)(?:_\d+)?)"
    match = re.search(qa_pattern, filename)
    if match:
        return (match.group(1), match.group(2))
        
    logging.warning(f"Could not extract dataset info from filename: {filename}")
    return None

def test_extract_dataset_type():
    """Test the dataset type extraction with various filenames"""
    test_files = [
        # Regular structure files
        "level_count_university_structure_small.json",
        "level_nodes_university_structure_medium_2.json",
        "level_count_university_structure_large_2.json",
        
        # Bullshit structure files
        "level_count_university_bullshit_structure_medium_2.json",
        "level_nodes_university_bullshit_structure_small.json",
        "level_count_university_bullshit_structure_large_2.json",
        
        # Task files - regular structure
        "Task_JSON_SubTask_level_count_Domain_university_structure_small_ExampleType_ZeroShot_20250213_233628.json",
        "Task_JSON_SubTask_level_nodes_Domain_university_structure_medium_2_ExampleType_ZeroShot_20250215_042943",
        
        # Task files - bullshit structure
        "Task_JSON_SubTask_level_count_Domain_university_bullshit_structure_large_2_ExampleType_ZeroShot_20250215_042939.json",
        "Task_JSON_SubTask_level_nodes_Domain_university_bullshit_structure_medium_2_ExampleType_ZeroShot_20250215_042943"
    ]
    
    print("\nTesting dataset type extraction:")
    for filename in test_files:
        result = extract_dataset_type(filename)
        print(f"\nFilename: {filename}")
        print(f"Extracted type: {result}")

def parse_question_from_user_prompt(user_prompt):
    """
    Extract the question from UserPrompt in different formats.

    This function will:
    1. Check if it's a "List all" question (e.g., "List all Program in the X..")
    2. Otherwise, for question words like 'How many', 'What is', 'Who is', 'Where', etc.,
       we look from that marker until we hit a question mark (?) or the string end.
    3. We optionally allow a period and/or space or newline after the question mark.
    4. Return the substring as the extracted question.
    """
    if not user_prompt:
        return None
        
    # -------------------------------
    # 1) Check if it's a "List all" format
    # -------------------------------
    if "List " in user_prompt:
        start_marker = "List "
        # We'll accept up to TWO consecutive periods or the newline
        potential_endings = ["..\n", "..", ".\n", "\n"]
        
        start_index = user_prompt.find(start_marker)
        if start_index != -1:
            # We'll try each potential ending in order
            end_index = len(user_prompt)
            for ending in potential_endings:
                possible_end = user_prompt.find(ending, start_index)
                if possible_end != -1:
                    end_index = min(end_index, possible_end)
            return user_prompt[start_index:end_index].strip(". \n")

    # -------------------------------
    # 2) Check for "How many" | "What is" | "Who is" | "Where" ...
    # -------------------------------
    question_markers = [
        "How many", "What is", "Who is", "Which", "Where"
    ]
    for marker in question_markers:
        if marker in user_prompt:
            start_index = user_prompt.find(marker)
            # We look for the question mark first
            qm_index = user_prompt.find("?", start_index)
            # If no question mark, fallback to period or end of string
            if qm_index == -1:
                qm_index = user_prompt.find(".", start_index)
            if qm_index == -1:
                qm_index = len(user_prompt)
            
            # Expand just beyond the question mark to catch a trailing period or space
            end_index = qm_index + 1
            if end_index < len(user_prompt) and user_prompt[end_index] in [".", " "]:
                end_index += 1
            
            # If there's a newline afterwards, skip it too
            if end_index < len(user_prompt) and user_prompt[end_index] in ["\n", "\r"]:
                end_index += 1
            
            # Return the substring
            return user_prompt[start_index:end_index].strip()

    # -------------------------------
    # 3) Fallback if no recognized format
    # -------------------------------
    return None


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
    
    # Create output folder
    os.makedirs(output_path, exist_ok=True)
    
    # Read QA dataset organized by dataset type
    qa_data = {}
    for filename in os.listdir(qa_path):
        if filename.endswith('.json'):
            dataset_type = extract_dataset_type(filename)
            if dataset_type:
                logger.info(f"Loading QA data from {filename} with type {dataset_type}")
                with open(os.path.join(qa_path, filename), 'r', encoding='utf-8') as f:
                    qa_json = json.load(f)
                    if dataset_type not in qa_data:
                        qa_data[dataset_type] = {}
                    
                    for item in qa_json:
                        if "question" in item:
                            normalized_question = normalize_question(item["question"])
                            qa_data[dataset_type][normalized_question] = item["answer"]
            else:
                logger.warning(f"Could not extract dataset type from QA file: {filename}")

    # Update results files
    for filename in os.listdir(results_path):
        if filename.endswith('.json'):
            try:
                dataset_type = extract_dataset_type(filename)
                if not dataset_type:
                    logger.warning(f"Could not extract dataset type from results file: {filename}")
                    continue
                
                if dataset_type not in qa_data:
                    logger.warning(f"No matching QA data found for dataset type: {dataset_type}")
                    continue

                input_file = os.path.join(results_path, filename)
                output_file = os.path.join(output_path, filename)
                
                logger.info(f"Processing file {filename} with dataset type {dataset_type}")
                
                with open(input_file, 'r', encoding='utf-8') as f:
                    results_json = json.load(f)
                
                # Update each result
                for item in results_json:
                    if "UserPrompt" in item:
                        question = parse_question_from_user_prompt(item["UserPrompt"])
                        if question:
                            normalized_question = normalize_question(question)
                            if normalized_question in qa_data[dataset_type]:
                                item["TrueAnswer"] = qa_data[dataset_type][normalized_question]
                                logger.info(f"Updated question: {normalized_question}")
                                logger.info(f"New TrueAnswer: {item['TrueAnswer']}")
                            else:
                                logger.warning(f"No match found for question '{normalized_question}' in dataset type {dataset_type}")

                # Save updated results
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results_json, f, indent=4, ensure_ascii=False)
                logger.info(f"Updated file saved: {output_file}")
                
            except Exception as e:
                logger.error(f"Error processing file {filename}: {str(e)}")
                continue
    
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
    
    # Read QA dataset once, organized by BOTH task type AND dataset name
    qa_data = {}  # Structure: qa_data[task_type][dataset_name][normalized_question] = answer
    for filename in os.listdir(qa_path):
        if not filename.endswith('.json'):
            continue
            
        dataset_info = extract_dataset_info(filename)
        if not dataset_info:
            logger.warning(f"Could not extract dataset info from QA file: {filename}")
            continue
            
        task_type, dataset_name = dataset_info
        if task_type not in qa_data:
            qa_data[task_type] = {}
        if dataset_name not in qa_data[task_type]:
            qa_data[task_type][dataset_name] = {}
            
        # Load QA data
        try:
            with open(os.path.join(qa_path, filename), 'r', encoding='utf-8') as f:
                qa_json = json.load(f)
                for item in qa_json:
                    if "question" in item:
                        normalized_q = normalize_question(item["question"])
                        qa_data[task_type][dataset_name][normalized_q] = item["answer"]
                logger.info(f"Loaded QA data for {task_type}/{dataset_name} from {filename}")
        except Exception as e:
            logger.error(f"Error loading QA file {filename}: {str(e)}")

    def process_directory(current_path, relative_path=""):
        """Recursively process directories and update JSON files"""
        current_output_path = os.path.join(output_base_path, relative_path)
        os.makedirs(current_output_path, exist_ok=True)
        
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            relative_item_path = os.path.join(relative_path, item)
            
            if os.path.isdir(item_path):
                process_directory(item_path, relative_item_path)
            elif item.endswith('.json'):
                try:
                    # Extract both task type and dataset name
                    dataset_info = extract_dataset_info(item)
                    if not dataset_info:
                        logger.warning(f"Could not extract dataset info from results file: {item}")
                        continue
                        
                    task_type, dataset_name = dataset_info
                    if task_type not in qa_data or dataset_name not in qa_data[task_type]:
                        logger.warning(f"No QA data found for {task_type}/{dataset_name}")
                        continue

                    logger.info(f"Processing file {item} ({task_type}/{dataset_name})")
                    
                    # Process the results file
                    with open(item_path, 'r', encoding='utf-8') as f:
                        results_json = json.load(f)
                    
                    # Update each result
                    for result_item in results_json:
                        if "UserPrompt" in result_item:
                            question = parse_question_from_user_prompt(result_item["UserPrompt"])
                            if question:
                                normalized_q = normalize_question(question)
                                if normalized_q in qa_data[task_type][dataset_name]:
                                    result_item["TrueAnswer"] = qa_data[task_type][dataset_name][normalized_q]
                                    logger.info(f"Updated {task_type}/{dataset_name} question: {normalized_q}")
                                    logger.info(f"New TrueAnswer: {result_item['TrueAnswer']}")
                                else:
                                    logger.warning(
                                        f"No match for question in {task_type}/{dataset_name}: {normalized_q}"
                                    )
                    
                    # Save updated file
                    output_file_path = os.path.join(current_output_path, item)
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        json.dump(results_json, f, indent=4, ensure_ascii=False)
                    logger.info(f"Saved updated file: {output_file_path}")
                    
                except Exception as e:
                    logger.error(f"Error processing {item_path}: {str(e)}")

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
    
    corrected_QA_dataset_path = "./dataset/JSON/QA/level_count"
    results_base_path = "./Results/JSON/level_count"
    output_base_path = "./Results/JSON/level_count_new"
    
    # Add debug call before processing
    #debug_question_matching(corrected_QA_dataset_path, results_base_path)
    
    process_nested_folders(corrected_QA_dataset_path, results_base_path, output_base_path)
    #update_results(corrected_QA_dataset_path, results_base_path, output_base_path)
    #correct_answers_QA_dataset(dataset_file_path, correct_QA, corrected_QA_dataset_path)

    #update_results(corrected_QA_dataset_path, result_file_path, output_results_folder_path)
