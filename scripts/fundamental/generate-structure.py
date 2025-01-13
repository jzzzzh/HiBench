import os
import pickle
import random
import sys

import numpy as np

sys.path.append('.')
from config.generator.fundamental import path as fundamental_path
from config.generator.fundamental import norm_generation_args, binary_generation_args
from generator.fundamental.structure import Generator


random.seed(6703)
np.random.seed(6703)
    

def main(path, args, replace=False):
    generator = Generator()
    for arg in args:
        for difficulty, dataset in generator(**arg):
            n = sum([len(data) for data in dataset.values()])
            print(f'generate {n} structures for {difficulty}')
            name = f"{'binary' if arg['binary'] else 'normal'}/{'balanced' if arg['balance'] else 'unbalanced'}-{'weighted' if arg['weights'] else 'unweighted'}-{difficulty}.pkl"
            filepath = os.path.join(path, name)
            if os.path.exists(filepath):
                print(f'file `{filepath}` exists, if you want to overwrite it please set replace to `True`.')
                continue
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                pickle.dump(dataset, f)


if __name__ == '__main__':
    main(fundamental_path, norm_generation_args)
    main(fundamental_path, binary_generation_args)
    