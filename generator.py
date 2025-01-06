# TODO: add calling of generation function of other task to build a unify generation script.
import os
import pickle
import random

import numpy as np

import configs
import generator.fundamental.generator as fundamental_generator
import generator.fundamental.tree_to_hierarchy_text as fundamental_tree_to_hierarchy_text

random.seed(6710)
np.random.seed(6710)
    

def main(path, args):
    path = os.path.join(path, 'structure')
    os.makedirs(path, exist_ok=True)
    for arg in args:
        for name, dataset in fundamental_generator(**arg):
            n = sum([len(data) for data in dataset.values()])
            print(f'generate {n} structures for {name}')
            # store pickle of dataset dict
            filepath = os.path.join(path, name + '.pkl')
            with open(filepath, 'wb') as f:
                pickle.dump(dataset, f)
            # store visualized dataset dict
            filepath = filepath[:-4] + '.txt'
            with open(filepath, 'w') as f:
                for scale, structures in dataset.items():
                    for structure in structures:
                        f.write(str(scale) +'\n')
                        f.write(fundamental_tree_to_hierarchy_text(structure) +'\n')


if __name__ == '__main__':
    main(configs.dataset_path, configs.generation_args)
    
    