import random
from typing import List

import networkx as nx


# AUX function.
def get_height(G, node) -> int:
    if G.out_degree(node) == 0: 
        return 1
    child_heights = [get_height(G, child) for child in G.neighbors(node)]
    return max(child_heights) + 1


def generate_another_structure(G):
    G_new = G.copy()
    for u, v, data in G_new.edges(data=True):
        if 'weight' in data:
            data['weight'] = random.randint(1, 29)  
    if random.random() < 0.5:
        edges = list(G_new.edges())
        num_edges_to_remove = random.randint(1, min(3, len(edges)))
        for _ in range(num_edges_to_remove):
            edge_to_remove = random.choice(edges)
            G_new.remove_edge(edge_to_remove[0], edge_to_remove[1])
            edges.remove(edge_to_remove)
    return G_new


# Normal Tasks
def add_node(G, node, parent) -> nx.Graph:
    G_result = G.copy()
    G_result.add_node(node)
    G_result.add_edge(parent, node)
    return G_result


def all_ancestor(G, node) -> List[str]:
    ancestors = set(G.predecessors(node))
    for ancestor in list(ancestors):
        ancestors.update(all_ancestor(G, ancestor))
    return ancestors


def all_children(G, node):
    successors = set(G.successors(node))
    for successor in list(successors):
        successors.update(all_children(G, successor))
    return successors


def remove_node(G, node) -> nx.Graph:
    G_result = G.copy()
    root = get_tree_root(G_result)

    if node != root:
        parents = list(G_result.predecessors(node))
        parent = parents[0] if parents else None
    else:
        parent = None
    children = list(G_result.successors(node))
    if parent != None:
        for child in children:
            G_result.add_edge(parent, child)
    else:
        new_root = children[0]
        for sibling in children[1:]:
            G_result.add_edge(new_root, sibling)
    
    G_result.remove_node(node)
    return G_result


def find_common_ancestor(G, selected_nodes) -> nx.Graph.nodes:
    node1 = selected_nodes[0]
    node2 = selected_nodes[1]
    root = get_tree_root(G)
    path1 = nx.shortest_path(G, source=root, target=node1)
    path2 = nx.shortest_path(G, source=root, target=node2)
    common_ancestor = None
    for node in path1:
        if node in path2:
            common_ancestor = node
    return common_ancestor


def is_isomorphic(G1, G2) -> bool:
    return nx.is_isomorphic(G1, G2)


def get_node_depth(G, node):
    return int(get_height(G, node))


def is_leaf_node(G, node):
    return G.out_degree(node) == 0


def get_tree_root(G, is_directed = True):
    # only consider the case when the graph is directed
    if is_directed:
        roots = [node for node, degree in G.in_degree() if degree == 0]
        if len(roots) == 1:
            return roots[0]
        elif len(roots) > 1:
            raise ValueError("Multiple possible root nodes found. The graph may not represent a single tree.")
        else:
            raise ValueError("No root node found. The graph may not be a tree or may be disconnected.")


# Binary Tasks.
def is_balanced_tree(G):
    
    def check_balance(node):
        if node is None:
            return 0, True
        left_child = None
        right_child = None
        for neighbor in G.neighbors(node):
            if G[node][neighbor].get('left', False):
                left_child = neighbor
            elif G[node][neighbor].get('right', False):
                right_child = neighbor
        left_height, is_left_balanced = check_balance(left_child)
        right_height, is_right_balanced = check_balance(right_child)
        current_balance = abs(left_height - right_height) <= 1
        is_balanced = is_left_balanced and is_right_balanced and current_balance
        current_height = max(left_height, right_height) + 1
        return current_height, is_balanced
    
    root = get_tree_root(G)
    _, balanced = check_balance(root)
    return balanced


def prefix_traversal(G):
    
    def traverse(node):
        if node is None:
            return []
        traversal = [node]
        left_child = None
        right_child = None
        for neighbor in G.neighbors(node):
            if G[node][neighbor].get('left', False):
                left_child = neighbor
            elif G[node][neighbor].get('right', False):
                right_child = neighbor
        traversal.extend(traverse(left_child))
        traversal.extend(traverse(right_child))
        return traversal

    root = get_tree_root(G)
    return traverse(root)


def infix_traversal(G):
    
    def traverse(node):
        if node is None:
            return []
        left_child = None
        right_child = None
        for neighbor in G.neighbors(node):
            if G[node][neighbor].get('left', False):
                left_child = neighbor
            elif G[node][neighbor].get('right', False):
                right_child = neighbor
        traversal = []
        traversal.extend(traverse(left_child))
        traversal.append(node)
        traversal.extend(traverse(right_child))
        return traversal

    root = get_tree_root(G)
    return traverse(root)


def postfix_traversal(G):
    
    def traverse(node):
        if node is None:
            return []
        left_child = None
        right_child = None
        for neighbor in G.neighbors(node):
            if G[node][neighbor].get('left', False):
                left_child = neighbor
            elif G[node][neighbor].get('right', False):
                right_child = neighbor
        traversal = []
        traversal.extend(traverse(left_child))
        traversal.extend(traverse(right_child))
        traversal.append(node)
        return traversal

    root = get_tree_root(G)
    return traverse(root)


def check_traversal_type(G):
    types = ['preorder', 'inorder', 'postorder']
    traversal_type = random.choice(types)
    if traversal_type == 'preorder':
        sequence = prefix_traversal(G)
    elif traversal_type == 'inorder':
        sequence = infix_traversal(G)
    else:
        sequence = postfix_traversal(G)
    return traversal_type, sequence


def construct_mirror_tree(G):
    # TODO: need debug
    def mirror_subtree(node, mirrored_graph):
        if node is None:
            return
        for neighbor in G.neighbors(node):
            edge_attrs = G[node][neighbor]
            if edge_attrs.get('left', False):
                mirrored_graph.add_edge(node, neighbor, right=True)
                mirror_subtree(neighbor, mirrored_graph)
            elif edge_attrs.get('right', False):
                mirrored_graph.add_edge(node, neighbor, left=True)
                mirror_subtree(neighbor, mirrored_graph)
    
    root = get_tree_root(G)
    mirrored_G = nx.DiGraph()
    mirror_subtree(root, mirrored_G)
    return mirrored_G