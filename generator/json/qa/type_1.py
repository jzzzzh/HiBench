"""
Question_1: "How many subjects does Computing Dept have?" 

Direction: How many node N2 does node N1 have.

"""

import os
import random
import json
from collections import defaultdict


# main function
def gen_anwser_type_1(scenario: str):
    if scenario == "company":
        pass #Todo
    elif scenario == "university":
        # read the university json file
        file_path = os.path.join(
            os.path.dirname(__file__), "..", "dataset", "university_structure.json"
        )
        json_data = read_json_file(file_path)
        node1, node2, children_count = get_random_nodes_and_child_count(json_data)

        # genearte question anwser pair
        question = f"How many {node2} does {node1} have?"
    elif scenario == "biology":
        pass #Todo
    else:
        raise ValueError("Invalid scenario.")

    return question, children_count


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


def get_random_nodes_and_child_count(data):
    keys_by_depth = gather_keys_by_depth(data)

    if not keys_by_depth or len(keys_by_depth) < 2:
        return None, None, 0

    random_depths = random.sample(list(keys_by_depth.keys()), 2)
    depth1, depth2 = random_depths[0], random_depths[1]

    random_node1_key = random.choice(keys_by_depth[random_depths[0]])
    random_node1_value = find_value_by_key(data, random_node1_key)
    random_node2_key = random.choice(keys_by_depth[random_depths[1]])

    if depth1 > depth2:
        return random_node1_key, random_node2_key, None
    elif depth1 == depth2:
        return random_node1_key, random_node2_key, 0
    else:
        return random_node1_key, random_node2_key, len(keys_by_depth[depth2])


def find_value_by_key(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                found_value = find_value_by_key(value, target_key)
                if found_value is not None:
                    return found_value
    elif isinstance(data, list):
        for item in data:
            found_value = find_value_by_key(item, target_key)
            if found_value is not None:
                return found_value
    return None


# read json file
def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    question, children_count = gen_anwser_type_1("university")
    print(question, children_count)
