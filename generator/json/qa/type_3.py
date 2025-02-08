"""
**Question_3**: "How many departments does a university has?" 
**Direction**: How many nodes in level x.

"""

import os
import random
import json
from collections import defaultdict


# main function
def gen_anwser_type_3(scenario: str):
    if scenario == "company":
        pass
    elif scenario == "university":
        # read the university json file
        file_path = os.path.join(
            os.path.dirname(__file__), "..", "dataset", "university_structure.json"
        )
        json_data = read_json_file(file_path)
        keys_by_depth, node_count = get_random_level_and_node_count(json_data)

        # genearte question anwser pair
        question = f"How many {keys_by_depth} does {scenario} have?"
    elif scenario == "biology":
        pass
    else:
        raise ValueError("Invalid scenario.")

    return question, node_count


def gather_keys_by_depth(data, current_depth=0, keys_by_depth=None):
    if keys_by_depth is None:
        keys_by_depth = defaultdict(list)

    if isinstance(data, dict):
        for key, value in data.items():
            keys_by_depth[current_depth].append(key)
            if isinstance(value, (dict, list)):
                gather_keys_by_depth(value, current_depth + 1, keys_by_depth)

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                gather_keys_by_depth(item, current_depth + 1, keys_by_depth)

    return keys_by_depth


def get_random_level_and_node_count(data):
    keys_by_depth = gather_keys_by_depth(data)

    if not keys_by_depth:
        return None, 0

    random_depth = random.choice(list(keys_by_depth.keys()))
    node_key = keys_by_depth[random_depth][0]
    node_count = len(keys_by_depth[random_depth])

    return node_key, node_count


# read json file
def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    question, node_count = gen_anwser_type_3("university")
    print(question, node_count)

#Bugs?
#How many University does university have? 2
#How many Department Name does university have? 26