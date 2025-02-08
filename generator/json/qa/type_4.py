"""
Question_4: "Does Dr. Peter teach Student Jason?" 

Direction: Relationship between two nodes.
"""

import os
import random
import json
from collections import defaultdict


# main function
def gen_anwser_type_4(scenario: str):
    if scenario == "company":
        pass
    elif scenario == "university":
        # read the university json file
        file_path = os.path.join(
            os.path.dirname(__file__), "..", "dataset", "university_structure.json"
        )
        json_data = read_json_file(file_path)
        parent, child = generate_random_question(json_data)

        # genearte question anwser pair
        question = f"Does {parent} teach {child}?"
    elif scenario == "biology":
        pass
    else:
        raise ValueError("Invalid scenario.")

    return question, True


def gather_possible_pairs(data, parent_value=None):
    pairs = []

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                if parent_value:
                    pairs.append((parent_value, value))
                parent_value = value
            if isinstance(value, (dict, list)):
                pairs.extend(gather_possible_pairs(value, parent_value))

    elif isinstance(data, list):
        for item in data:
            pairs.extend(gather_possible_pairs(item, parent_value))

    return pairs


def generate_random_question(data):
    pairs = gather_possible_pairs(data)

    if not pairs:
        raise ValueError("No suitable pairs found.")

    parent, child = random.choice(pairs)
    return parent, child


# read json file
def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    question, answer = gen_anwser_type_4("university")
    print(question, answer)
