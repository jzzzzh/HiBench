import math
import random
import warnings
from typing import Callable
from functools import partial

import numpy as np
import networkx as nx


def find_root(graph):
    for node in graph.nodes:
        if graph.in_degree(node) == 0:
            return node
    return None


def tree_to_hierarchy_text(graph, node=None, prefix="", visited=None, is_last=True, is_root=True):
    if visited is None:
        visited = set()  # Initialize a set to track visited nodes

    if node is None:
        node = find_root(graph)
        if node is None:
            raise ValueError("The graph has no root; it may not be a valid tree.")

    # If the node has already been visited, mark it as a duplicate
    if node in visited:
        return f"{prefix}{'`-- ' if not is_root else ''}{node} (duplicate)\n"

    # Mark the current node as visited
    visited.add(node)

    # Build the current node's representation
    result = f"{prefix}{'' if is_root else ('`-- ' if is_last else '|-- ')}{node}\n"

    # Get children of the current node
    children = list(graph.successors(node))
    for i, child in enumerate(children):
        child_is_last = (i == len(children) - 1)
        # Adjust the prefix for the child nodes
        child_prefix = prefix + ("    " if is_last and not is_root else "|   ")
        # Recursively process child nodes
        result += tree_to_hierarchy_text(graph, node=child, prefix=child_prefix, visited=visited, is_last=child_is_last, is_root=False)
    
    return result


def weight_fn(weight):
    return round(random.uniform(*weight), 1) if weight else None


def generator(num, balance, scales, weight, binary):
    weight_func = partial(weight_fn, weight=weight)
    for difficulty, scale in scales.items():
        if binary:
            check_binary(scale)
        name = format_filename(balance=balance, weight=weight, binary=binary, difficulty=difficulty)
        dataset = gen_datapool(
            num, directed=True, M_range=scale['L'], MAX_D_range=scale['D'],
            weight_func=weight_func, balance=balance, filter_homographic=False, verbose=True
        )
        yield name, dataset


def check_binary(scale):
    D = list(scale['D'])
    if min(D) !=2 and min(D) != max(D):
        raise ValueError('degree argument is not binary')



def calculate_node_range(d, L):
    if d == 1:
        return L, L
    else:
        return L, (1 - d**L) // (1 - d) + 1


def format_filename(balance, weight, binary, difficulty):
    return f"{'binary' if binary else 'normal'}-{'balanced' if balance else 'unbalanced'}-{'weighted' if weight else 'unweighted'}-{difficulty}"


def gen_datapool(num, directed = True, M_range: int = 5, MAX_D_range:int = 3, weight_func: Callable = lambda:None, balance: bool=True, filter_homographic=True, randbare_max = 50, verbose = False):
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

    filter_homographic: bool, True to ensure all trees in the datapool are isomorphic, **very costy**

    randbare_max: when filter_homographics, quit after randbare_max failed trials

    verbose: bool
    '''
    tree_datapool = {}
    for M in M_range:
        for MAX_D in MAX_D_range:
            n_range = list(range(*calculate_node_range(MAX_D, M)))
            for tmp_N in sorted(np.random.choice(n_range, min(len(n_range), num), replace=False)):
                # print(tmp_N, M)
                N = int(tmp_N)
                tree_datapool[(N, M, MAX_D)] = []
                for _ in range(num):
                    tree_datapool[(N, M, MAX_D)].append(generate_tree(N, M, MAX_D, directed, balanced=balance, shuffled=True, weight_func=weight_func, seed=random.randint(0, 100000)))
                if filter_homographic:
                    if verbose:
                        print(f"Filtering isomorphic trees for N={N}, M={M}, D={MAX_D}...")
                    for _ in range(randbare_max):
                        tree = generate_tree(N, M, MAX_D, directed, balanced=False, shuffled=False, weight_func=weight_func)
                        isomorphic = False
                        for t in tree_datapool[(N, M, MAX_D)]:
                            if nx.is_isomorphic(tree, t):
                                isomorphic = True
                                break
                        if not isomorphic:
                            tree_datapool[(N, M, MAX_D)].append(tree)
                    if verbose:
                        print(f"Finally obtain {len(tree_datapool[(N, M, MAX_D)])} trees.")
    return tree_datapool


def generate_tree(N, M, MAX_D = 2, directed = True, balanced = False, shuffled = False, weight_func: Callable = lambda:None, seed = None):
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