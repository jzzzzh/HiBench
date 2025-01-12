NUM_PER_CATEGORY = 3

path = './dataset/Fundamental'


norm_scales = {'easy': {'L': range(2, 4), 'D': range(2, 4)},
        'medium-1': {'L': range(2, 4), 'D': range(3, 5)},
        'medium-2': {'L': range(3, 5), 'D': range(2, 4)},
        'hard-1': {'L': range(2, 4), 'D': range(5, 7)},
        'hard-2': {'L': range(5, 7), 'D': range(2, 4)}}

binary_scale = {'easy': {'L': range(2, 5), 'D': range(2, 3)},
        'medium': {'L': range(5, 8), 'D': range(2, 3)},
        'hard': {'L': range(8, 10), 'D': range(2, 3)}}

norm_generation_args = [
    {
        'num': NUM_PER_CATEGORY,
        'balance': False,
        'weights': None,
        'binary': False,
        'scales': norm_scales
    }
]

binary_generation_args = [
    {
        'num': NUM_PER_CATEGORY,
        'balance': False,
        'weights': None,
        'binary': True,
        'scales': binary_scale
    },
    {
        'num': NUM_PER_CATEGORY,
        'balance': True,
        'weights': None,
        'binary': True,
        'scales': binary_scale
    },
]