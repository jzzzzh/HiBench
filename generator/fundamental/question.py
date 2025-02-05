import random

from .algo import *
from .literalizer import *


def add_node_qa(G):
    node = len(G.nodes)
    parent = random.sample(list(G.nodes), 1)[0]
    ref_ans = add_node(G, node, parent)
    return {
        'add_node_Q': f'add a new node {node} as a child to the node {parent} in the given structure.',
        'add_node_A_E': edge_presentation(ref_ans),
        'add_node_A_H': hierarchy_presentation(ref_ans),
    }
    
def all_ancestor_qa(G):
    q_node = random.sample(list(G.nodes), 1)[0]
    ref_ans = all_ancestor(G, q_node)
    return {
        'all_ancestor_Q': f'please find out all the ancestor of node {q_node}.',
        'all_ancestor_A': ', '.join(map(str, ref_ans)) if ref_ans else 'None'
    }
    
def all_children_qa(G):
    q_node = random.sample(list(G.nodes), 1)[0]
    ref_ans = all_children(G, q_node)
    return {
        'all_children_Q': f'please find out all the children of node {q_node}.',
        'all_children_A': ', '.join(map(str, ref_ans)) if ref_ans else 'None'
    }
    
def common_ancestor_qa(tree):
    q_nodes = random.sample(list(tree.nodes), 2)
    ref_ans = find_common_ancestor(tree, q_nodes)
    return {
        'common_ancestor_Q': f'determine the lowest common ancestor of the nodes {q_nodes[0]} and {q_nodes[1]} within the structure.',
        'common_ancestor_A': ref_ans,
    }
    
    
def isomorphic_qa(G):
    G_new = generate_another_structure(G)
    ref_ans = is_isomorphic(G, G_new)
    return {
        'isomorphic_Q_E': f'and another hierarchical structure: {edge_presentation(G_new)}, please decide whether the given two structure are isomorphic or not.',
        'isomorphic_Q_H': f'and another hierarchical structure: {hierarchy_presentation(G_new)}, please decide whether the given two structure are isomorphic or not.',
        'isomorphic_A': ref_ans,
    }
    
    
def remove_node_qa(G):
    q_node = random.sample(list(G.nodes), 1)[0]
    ref_ans = remove_node(G, q_node)
    return {
        'remove_node_Q': f'please remove the node {q_node} from the given structure. Output the updated structure following the input structure format.',
        'remove_node_A_E': edge_presentation(ref_ans),
        'remove_node_A_H': hierarchy_presentation(ref_ans),
    }
    
    
def node_depth_qa(G):
    q_node = random.sample(list(G.nodes), 1)[0]
    ref_ans = get_node_depth(G, q_node)
    return {
        'node_depth_Q': f'determine the depth of the node {q_node} within the structure, where the root node is assigned a depth of 1.',
        'node_depth_A': ref_ans,
    }
    
    
def leaf_qa(G):
    q_node = random.sample(list(G.nodes), 1)[0]
    ref_ans = is_leaf_node(G, q_node)
    return {
        'leaf_Q': f'is node {q_node} a leaf node?',
        'leaf_A': ref_ans,
    }
    
def root_qa(G):
    ref_ans = find_root(G)
    return {
        'root_Q': f'which node is the root?',
        'root_A': ref_ans,
    }
    
    
def balance_qa(G):
    ref_ans = is_balanced_tree(G)
    return {
        'balance_Q': f'determine whether it is a balanced tree?',
        'balance_A': ref_ans,
    }
    
def prefix_traversal_qa(G):
    ref_ans = prefix_traversal(G)
    return {
        'prefix_traversal_Q': f'generate the traversal sequence in prefix order (preorder), where the nodes are visited in the order: root, left subtree, and right subtree.',
        'prefix_traversal_A': ref_ans,
    }
    
def infix_traversal_qa(G):
    ref_ans = infix_traversal(G)
    return {
        'infix_traversal_Q': f'generate the traversal sequence in infix order (inorder), where the nodes are visited in the order: left subtree, root, and right subtree.',
        'infix_traversal_A': ref_ans,
    }
    
def postfix_traversal_qa(G):
    ref_ans = postfix_traversal(G)
    return {
        'postfix_traversal_Q': f'generate the traversal sequence in postfix order (postorder), where the nodes are visited in the order: left subtree, right subtree, and root.',
        'postfix_traversal_A': ref_ans,
    }
    
def traversal_order_verification_qa(G):
    ref_ans, sequence = check_traversal_type(G)
    return {
        'traversal_order_verification_Q': f'and a traversal sequence {sequence}, verify if it is the preorder, inorder, and postorder consistent with the tree.',
        'traversal_order_verification_A': ref_ans,
    }
    
def mirror_tree_qa(G):
    ref_ans = construct_mirror_tree(G)
    return {
        'mirror_tree_Q': f'generate the mirror image of the tree, where the left and right children of all nodes are swapped.',
        'mirror_tree_A_E': binary_edge_presentation(ref_ans),
        'mirror_tree_A_H': binary_hierarchy_presentation(ref_ans),
    }