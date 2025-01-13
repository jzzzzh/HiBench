import math
import random
import warnings
from typing import Callable

import numpy as np
import networkx as nx


class Generator(object):
    
    def __init__(self):
        pass
    
    def __call__(self, num, scales, balance=False, weights=False, binary=False):
        assert isinstance(num, int)
        for difficulty, scale in scales.items():
            degrees, depths = list(scale['D']), list(scale['L'])
            assert len(degrees) == 1 and degrees[0] == 2 if binary else True # check width for binary tree
            assert len(weights) == 2 if weights else True
            weight_func = lambda: round(random.uniform(*weights), 1) if weights else None
            dataset = self.__gen_datapool(
                num, directed=True, M_range=depths, MAX_D_range=degrees, binary=binary,
                weight_func=weight_func, balance=balance)
            yield difficulty, dataset

    def __calculate_node_range(self, degree, depth):
        if degree == 1:
            return depth, depth
        else:
            return depth, (1 - degree**depth) // (1 - degree) + 1
        
    def __gen_datapool(self, num, directed = True, M_range: int = 5, MAX_D_range:int = 3, weight_func: Callable = lambda:None, balance: bool=True, binary=False):
        '''
        generate and return a tree datapool

        Parameters
        ----------
        directed: True for directed tree, False for undirected tree

        M_range: list of M (number of levels) for trees in the datapool

        MAX_D_range: list of D(number of degrees) for trees in the datapool

        weight_func: random weight generator, a function with no input and one single number output as weight of an edge, default return None

        modulation_dict: dictionary of {modulation: number}, interfering tree generation to ensure diversity and sufficient high hop cases. 
                Sum of values is the number of trees generated for each N M D.
            modulation: one string under following options, biasing tree generation to meet requirements such as more hops, 
                    this parameter has less priority than N, M or D, which means the effects are not guaranteed.
                'normal': randomly choose M levels for N nodes tree.
                '(s)balanced': The tree type is a balanced tree, 
                    'sbalanced' means the edges in the balance tree may not directed to the same way.
                '(s)unbalanced': The tree type is an unbalanced tree, 
                    'sunbalanced' means the edges in the unbalanced tree may not directed to the same way.

        deprecate argument: filter_homographic: bool, True to ensure all trees in the datapool are isomorphic, **very costy**

        randbare_max: when filter_homographics, quit after randbare_max failed trials

        verbose: bool
        '''
        generate_func = generate_binary_tree if binary else generate_normal_tree
        tree_datapool = {}
        for M in M_range:
            for MAX_D in MAX_D_range:
                n_range = list(range(*self.__calculate_node_range(MAX_D, M)))
                for tmp_N in sorted(np.random.choice(n_range, min(len(n_range), num), replace=False)):
                    # print(tmp_N, M)
                    N = int(tmp_N)
                    tree_datapool[(N, M, MAX_D)] = []
                    for _ in range(num):
                        tree_datapool[(N, M, MAX_D)].append(generate_func(N, M, MAX_D, directed, balanced=balance, shuffled=True, weight_func=weight_func, seed=random.randint(0, 100000)))
        return tree_datapool


def max_nodes_in_tree(M, MAX_D):
    if MAX_D == 0:
        return 1  
    elif MAX_D == 1:
        return M  
    else:
        return (1 - MAX_D**M) // (1 - MAX_D) if MAX_D != 1 else M + 1
    
def get_min_degree(N, K, M, T, P, Q, MAXD):
    # print(N, K, M, T, P, Q, MAXD)
    # print(M-T)
    # if(M-T != 1):
        # print(((N-K)*(1-MAXD)-P*MAXD*(1-MAXD**(M-T)))/((1-MAXD**(M-T-1))*MAXD) - Q)
    if(M-T == 1):
        return max(0, N-K-P*MAXD)
    else:
        return max(0, math.ceil(((N-K)*(1-MAXD)-P*MAXD*(1-MAXD**(M-T)))/((1-MAXD**(M-T-1))*MAXD) - Q))

def get_max_degree(N, K, M, T, P, Q, MAXD):
    # print(MAX_D)
    # print(N-K+T-M+1)
    return min(MAXD, N-K+T-M+1) if min(MAXD, N-K+T-M+1) >= 0 else 0


def generate_normal_tree(N, M, MAX_D = 2, directed = True, balanced = False, shuffled = False, weight_func: Callable = lambda:None, seed = None):
    '''
    generate and return a nx.Graph or nx.DiGraph

    Parameters
    ----------
    N: number of nodes

    M: number of levels

    MAX_D: max number of node degree

    directed: True for directed Tree, False for undirected Tree

    balanced: True for balanced Tree, False for unbalanced Tree

    shuffled: True for shuffled Tree, False for unshuffled Tree

    weight_func: random weight generator, a function with no input and one single number output as weight of an edge, default return None

    seed: random seed

    ''' 
    if MAX_D < 0 or N < 0 or M < 0:
        raise ValueError("MAX_D, N or M less than 0.")
    if max_nodes_in_tree(M, MAX_D) < N:
        raise ValueError("Node number larger than max node number in tree.")
    
    if seed is not None:
        random.seed(seed)

    G = nx.DiGraph() if directed else nx.Graph()
    G.add_node(0)  # add root node
    remain_node_list = list(range(0, N))
    if shuffled:
        random.shuffle(remain_node_list)
        # print(remain_node_list)
    # current_level = [0]
    current_level = [remain_node_list[0]]
    node_count = 1
    
    for layer_num in range(M):
        if node_count >= N:
            break
        next_level = []
        # print(f"current_level{current_level}")
        current_level_num = len(current_level)-1
        next_level_num = 0
        for idx, parent in enumerate(current_level):
            my_N, my_K, my_M, my_T, my_P, my_Q, my_MAXD = N, node_count, M, layer_num + 1, current_level_num, next_level_num, MAX_D
            minDegree = get_min_degree(my_N, my_K, my_M, my_T, my_P, my_Q, my_MAXD)
            maxDegree = get_max_degree(my_N, my_K, my_M, my_T, my_P, my_Q, my_MAXD)
            minDegree = min(minDegree, N - node_count)
            minDegree = min(minDegree, MAX_D)
            # print("minDegree", minDegree)
            # print("maxDegree", maxDegree)
            degree = random.randint(minDegree, maxDegree)
            if balanced:
                degree = min(N - node_count//len(current_level), MAX_D)
                degree = min(degree, N - node_count)
            # if shuffled:
            #     children = random.sample(, degree)
            # else:
            # children = random.sample(range(node_count, node_count + degree), degree)
            # print(remain_node_list[node_count:node_count + degree], degree)
            children = random.sample(remain_node_list[node_count:node_count + degree], degree)
            # print("children", children)
            for child in children:
                if node_count < N and child < N:
                    G.add_node(child)
                    G.add_edge(parent, child)
                    # print(f"add edge {parent} -> {child}")
                    weight = weight_func()
                    if weight is not None:
                        G[parent][child]['weight'] = weight
                    next_level.append(child)
                    node_count += 1
                    next_level_num += 1
            current_level_num-=1

        current_level = next_level
    if node_count < N:
        print("*"*20)
        warnings.warn(f"Node number {N} not reached.")
        print("*"*20)
    return G


def generate_binary_tree(N, M, MAX_D=2, directed=True, balanced=False, shuffled=False, weight_func: Callable = lambda: None, seed=None):
    '''
    Generate and return a nx.Graph or nx.DiGraph.

    Parameters
    ----------
    N: int
        Number of nodes.

    M: int
        Number of levels.

    MAX_D: int
        Maximum number of node degree (must be 2 for binary tree).

    directed: bool
        True for directed tree, False for undirected tree.

    balanced: bool
        True for balanced tree, False for unbalanced tree.

    shuffled: bool
        True for shuffled node indices, False for sequential indices.

    weight_func: Callable
        Random weight generator, a function with no input and one single number output as weight of an edge, default returns None.

    seed: int or None
        Random seed.
    '''
    if balanced and N < 2**(M - 1):
        new_N = random.choice(range(2**(M - 1), 2**M))
        print(f"Insufficient nodes {N} to generate a balanced tree with the given {M} levels, resetting N to {new_N}.")
        N = new_N

    if MAX_D != 2:
        raise ValueError("MAX_D must be 2 for a binary tree.")
    if MAX_D < 0 or N < 0 or M < 0:
        raise ValueError("MAX_D, N, or M cannot be negative.")
    if seed is not None:
        random.seed(seed)

    G = nx.DiGraph() if directed else nx.Graph()
    G.add_node(0)
    remain_node_list = list(range(0, N))

    if shuffled:
        random.shuffle(remain_node_list)

    current_level = [remain_node_list[0]]
    node_count = 1

    for layer_num in range(M):
        if node_count >= N:
            break
        next_level = []
        current_level_num = len(current_level)-1
        next_level_num = 0
        for parent in current_level:
            if node_count >= N:
                break
            my_N, my_K, my_M, my_T, my_P, my_Q, my_MAXD = N, node_count, M, layer_num + 1, current_level_num, next_level_num, MAX_D
            minDegree = get_min_degree(my_N, my_K, my_M, my_T, my_P, my_Q, my_MAXD)
            maxDegree = get_max_degree(my_N, my_K, my_M, my_T, my_P, my_Q, my_MAXD)
            minDegree = min(minDegree, N - node_count)
            minDegree = min(minDegree, MAX_D)
            degree = random.randint(minDegree, maxDegree)
            if balanced:
                if layer_num < M - 1:
                    degree = MAX_D
                else:
                    degree = min(MAX_D, N - node_count)
            # print(f"minDegree: {minDegree}, maxDegree: {maxDegree}, degree: {degree}")
            # else:
            #     degree = random.randint(1, min(MAX_D, N - node_count))
            degree = min(degree, len(remain_node_list) - node_count)
            
            left_child_assigned, right_child_assigned = False, False
            children = random.sample(remain_node_list[node_count: node_count + degree], degree)
            for child in children:
                if node_count < N:
                    G.add_node(child)
                    G.add_edge(parent, child)
                    weight = weight_func()
                    if weight is not None:
                        G[parent][child]['weight'] = weight
                    if not left_child_assigned and not right_child_assigned:
                        side = random.choice(['left', 'right'])
                        G[parent][child][side] = True
                        if side == 'left':
                            left_child_assigned = True
                        else:
                            right_child_assigned = True
                    elif left_child_assigned and not right_child_assigned:
                        G[parent][child]['right'] = True
                        right_child_assigned = True
                    elif not left_child_assigned and right_child_assigned:
                        G[parent][child]['left'] = True
                        left_child_assigned = True
                    else:
                        raise RuntimeError('Unexpected condition: More than two child nodes assigned.')
                    next_level.append(child)
                    node_count += 1
                    next_level_num += 1
            current_level_num-=1
        current_level = next_level
    if node_count < N:
        print(f"Only {node_count} nodes were constructed for {M} level, fewer than requested {N}.")
    return G


if __name__ == "__main__":
    from literalizer import edge_presentation, binary_edge_presentation, binary_hierarchy_presentation, hierarchy_presentation
    generator = Generator()
    scales = {
        "easy": {"D": [2], "L": [3]},
        "medium": {"D": [2], "L": [3]},
        "hard": {"D": [2], "L": [5]},
    }
    for difficulty, dataset in generator(1, scales, balance=True, weights=[1, 10], binary=True):
        print(difficulty)
        for (N, M, MAX_D), graphs in dataset.items():
            print(f"N={N}, M={M}, MAX_D={MAX_D}")
            for graph in graphs:
                # print(edge_presentation(graph))
                print(binary_edge_presentation(graph))
                print()
        print()
