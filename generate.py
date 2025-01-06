# TODO: add calling of generation function of other task to build a unify generation script.
import os
import pickle
import random

import numpy as np

from config.generator.fundamental import path as fundamental_path
from config.generator.fundamental import norm_generation_args, binary_generation_args
from generator.fundamental.structure import Generator


random.seed(6710)
np.random.seed(6710)
    

def main(path, args, replace=False):
    generator = Generator()
    for arg in args:
        for difficulty, dataset in generator(**arg):
            n = sum([len(data) for data in dataset.values()])
            print(f'generate {n} structures for {difficulty}')
            # store pickle of dataset dict
            name = f"{'binary' if arg['binary'] else 'normal'}/{'balanced' if arg['balance'] else 'unbalanced'}-{'weighted' if arg['weights'] else 'unweighted'}-{difficulty}.pkl"
            filepath = os.path.join(path, name)
            if os.path.exists(filepath):
                print(f'file `{filepath}` exists, if you want to overwrite it please set replace to `True`.')
                continue
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                pickle.dump(dataset, f)
            # store visualized dataset dict
            # filepath = filepath[:-4] + '.txt'
            # with open(filepath, 'w') as f:
            #     for scale, structures in dataset.items():
            #         for structure in structures:
            #             f.write(str(scale) +'\n')
            #             f.write(fundamental_tree_to_hierarchy_text(structure) +'\n')


if __name__ == '__main__':
    main(fundamental_path, norm_generation_args)
    main(fundamental_path, binary_generation_args)
    