from typing import Any, Dict, List
import glob
import json
import os
import pickle
import sys
from multiprocessing import Pool

import yaml


sys.path.append('.')
from generator.fundamental.question import *
from generator.fundamental.literalizer import *


def generate_normal_qa(structures) -> List[Dict[str, Any]]:
    datasets = list()
    question_generators = [root_qa, all_ancestor_qa, all_children_qa, leaf_qa, isomorphic_qa, node_depth_qa, add_node_qa, remove_node_qa, common_ancestor_qa]
    count = 0
    for structure_args, structure_list in structures.items():
        for structure in structure_list:
            dataset = dict(
                structure_args = structure_args,
                id=count, 
                edge_presentation=edge_presentation(structure),
                hierarchy_presentation=hierarchy_presentation(structure)
                )
            count += 1
            for generate_qa in question_generators:
                dataset.update(generate_qa(structure))
            datasets.append(dataset)
    return datasets


def generate_binary_qa(structures) -> List[Dict[str, Any]]:
    datasets = list()
    question_generators = [balance_qa, prefix_traversal_qa, infix_traversal_qa, postfix_traversal_qa, traversal_order_verification_qa, mirror_tree_qa]
    count = 0
    for structure_args, structure_list in structures.items():
        for structure in structure_list:
            dataset = dict(
                structure_args = structure_args,
                id=count, 
                edge_presentation=binary_edge_presentation(structure),
                hierarchy_presentation=binary_hierarchy_presentation(structure)
                )
            count += 1
            for generate_qa in question_generators:
                dataset.update(generate_qa(structure))
            datasets.append(dataset)
    return datasets


def process_file(args):
    file, binary= args
    with open(file, 'rb') as f:
        structures = pickle.load(f)
    datasets = generate_binary_qa(structures) if binary else generate_normal_qa(structures)
    filename = file.replace('.pkl', '.json')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(datasets, f, indent=4)
        
        
            

def main():
    with open('./config/config.yaml', 'r') as file:
        configs = yaml.safe_load(file)
    
    binary_structure_path = os.path.join(configs['Dataset']['Fundamental']['Dir'], 'binary')
    normal_structure_path = os.path.join(configs['Dataset']['Fundamental']['Dir'], 'normal')

    files = glob.glob(os.path.join(binary_structure_path, '*.pkl'))
    binary_args = [(file, True) for file in files]
    with Pool(processes=16) as pool:
        pool.map(process_file, binary_args)

    files = glob.glob(os.path.join(normal_structure_path, '*.pkl'))
    normal_args = [(file, False) for file in files]
    with Pool(processes=16) as pool:
        pool.map(process_file, normal_args)

if __name__ == '__main__':
    main()