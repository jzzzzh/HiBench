"""
Question_2: "Which level does the node 'Computing Dept' in?" 

Direction: Depth of a node.

"""

import os
import random
import json
from collections import defaultdict


# main function
def gen_anwser_type_2(scenario: str):
    if scenario == "company":
        pass
    elif scenario == "university":
        # read the university json file
        file_path = os.path.join(
            os.path.dirname(__file__), "..", "dataset", "university_structure.json"
        )
        json_data = read_json_file(file_path)
        value, depth = get_random_value_and_depth(json_data)

        # genearte question anwser pair
        question = f"Which level does the node '{value}' in?"
    elif scenario == "biology":
        pass
    else:
        raise ValueError("Invalid scenario.")

    return question, depth


# Finding value depth by recursion
def gather_values_by_depth(data, current_depth=0, values_by_depth=None):
    if values_by_depth is None:
        values_by_depth = defaultdict(list)

    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, (dict, list)):
                gather_values_by_depth(value, current_depth + 1, values_by_depth)
            else:
                values_by_depth[current_depth].append(value)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                gather_values_by_depth(item, current_depth + 1, values_by_depth)
            else:
                values_by_depth[current_depth].append(item)

    return values_by_depth


def get_random_value_and_depth(data):
    values_by_depth = gather_values_by_depth(data)
    if not values_by_depth:
        return None, None

    random_depth = random.choice(list(values_by_depth.keys()))
    random_value = random.choice(values_by_depth[random_depth])

    return random_value, random_depth


# read json file
def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    question, depth = gen_anwser_type_2("university")
    print(question, depth)
