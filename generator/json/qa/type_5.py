"""
Question_5: "What is the university name?" 

Direction: What info is on leaf x.

"""

import os
import random
import json
from collections import defaultdict


# main function
def gen_anwser_type_5(scenario: str):
    if scenario == "company":
        pass
    elif scenario == "university":
        # read the university json file
        file_path = os.path.join(
            os.path.dirname(__file__), "..", "dataset", "university_structure.json"
        )
        json_data = read_json_file(file_path)
        random_key, random_value = get_random_string_key_value(json_data)

        # genearte question anwser pair
        question = f"What is the {random_key} name?"
    elif scenario == "biology":
        pass
    else:
        raise ValueError("Invalid scenario.")

    return question, random_value


def gather_string_key_value_pairs(data):
    pairs = []

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                pairs.append((key, value))
            elif isinstance(value, (dict, list)):
                pairs.extend(gather_string_key_value_pairs(value))

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                pairs.extend(gather_string_key_value_pairs(item))

    return pairs


def get_random_string_key_value(data):
    string_pairs = gather_string_key_value_pairs(data)

    if not string_pairs:
        return None, None

    return random.choice(string_pairs)


# read json file
def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    question, children_count = gen_anwser_type_5("university")
    print(question, children_count)
