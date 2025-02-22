import os
import json
import re


def clean_true_answer_in_file(file_path):
    """
    Cleans the 'TrueAnswer' field in a single JSON file and overwrites the file.

    Parameters:
        file_path (str): Path to the JSON file to be cleaned.
    """
    # Regex for matching valid complexities like O(n), O(n * m), etc.
    complexity_pattern = r"O\([^\)]+\)"

    try:
        # Load the JSON data
        with open(file_path, "r") as file:
            data = json.load(file)

        # Process each entry in the JSON
        for entry in data:
            if "TrueAnswer" in entry:
                # Extract and clean the TrueAnswer using regex
                match = re.search(complexity_pattern, entry["TrueAnswer"])
                entry["TrueAnswer"] = match.group(0) if match else ""
            elif "time" in entry:
                # for time
                match = re.search(complexity_pattern, entry["time"])
                entry["time"] = match.group(0) if match else ""
                # for space
                match = re.search(complexity_pattern, entry["space"])
                entry["space"] = match.group(0) if match else ""

        # Overwrite the original file with the cleaned data
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Processed and replaced file: {file_path}")

    except json.JSONDecodeError:
        print(f"Skipping invalid JSON file: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def clean_true_answer_in_folder_recursive(folder_path):
    """
    Cleans the 'TrueAnswer' field for all JSON files in a folder and its subfolders,
    overwriting the original files.

    Parameters:
        folder_path (str): Path to the folder containing JSON files.
    """
    # Walk through all files and subfolders in the folder
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):  # Process only JSON files
                print(filename)
                # Construct full path to the file
                file_path = os.path.join(root, filename)

                # Call the cleaning function for each file
                clean_true_answer_in_file(file_path)


if __name__ == "__main__":
    # Example usage:
    # Replace 'folder_path' with the path to the folder containing your JSON files
    clean_true_answer_in_folder_recursive("./Results/Code")
    clean_true_answer_in_folder_recursive("./dataset/Code")
