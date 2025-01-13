import sys
from unittest import TestCase

import networkx as nx

sys.path.append('.')
from generator.fundamental.algo import *


class TestBinaryTreeFunctions(TestCase):

    def setUp(self):
        self.trees = dict()
        # Balanced tree
        self.trees["balanced"] = self._build_tree([
            ('1', '2', {'left': True}),
            ('1', '3', {'right': True}),
            ('2', '4', {'left': True}),
            ('2', '5', {'right': True}),
            ('3', '6', {'left': True}),
            ('3', '7', {'right': True})
        ])
        # Unbalanced tree
        self.trees["unbalanced"] = self._build_tree([
            ('1', '2', {'left': True}),
            ('2', '3', {'left': True})
        ])
        # Larger balanced tree
        self.trees["large_balanced"] = self._build_tree([
            ('1', '2', {'left': True}),
            ('1', '3', {'right': True}),
            ('2', '4', {'left': True}),
            ('2', '5', {'right': True}),
            ('3', '6', {'left': True}),
            ('3', '7', {'right': True}),
            ('4', '8', {'left': True}),
            ('4', '9', {'right': True})
        ])

    def _build_tree(self, edges):
        tree = nx.DiGraph()
        for parent, child, attrs in edges:
            tree.add_edge(parent, child, **attrs)
        return tree

    def test_is_balanced_tree(self):
        self.assertTrue(is_balanced_tree(self.trees["balanced"]))
        self.assertFalse(is_balanced_tree(self.trees["unbalanced"]))
        self.assertTrue(is_balanced_tree(self.trees["large_balanced"]))

    def test_traversals(self):
        for name, tree in self.trees.items():
            with self.subTest(tree=name):
                if name == "balanced":
                    self.assertEqual(prefix_traversal(tree), ['1', '2', '4', '5', '3', '6', '7'])
                    self.assertEqual(infix_traversal(tree), ['4', '2', '5', '1', '6', '3', '7'])
                    self.assertEqual(postfix_traversal(tree), ['4', '5', '2', '6', '7', '3', '1'])
                elif name == "unbalanced":
                    self.assertEqual(prefix_traversal(tree), ['1', '2', '3'])
                    self.assertEqual(infix_traversal(tree), ['3', '2', '1'])
                    self.assertEqual(postfix_traversal(tree), ['3', '2', '1'])
                elif name == "large_balanced":
                    self.assertEqual(prefix_traversal(tree), ['1', '2', '4', '8', '9', '5', '3', '6', '7'])
                    self.assertEqual(infix_traversal(tree), ['8', '4', '9', '2', '5', '1', '6', '3', '7'])
                    self.assertEqual(postfix_traversal(tree), ['8', '9', '4', '5', '2', '6', '7', '3', '1'])

    def test_construct_mirror_tree(self):
        for name, tree in self.trees.items():
            with self.subTest(tree=name):
                mirrored_tree = construct_mirror_tree(tree)
                # Verify the mirrored structure for specific cases.
                if name == "balanced":
                    expected_edges = [
                        ('1', '2', {'right': True}), ('1', '3', {'left': True}),
                        ('2', '4', {'right': True}), ('2', '5', {'left': True}),
                        ('3', '6', {'right': True}), ('3', '7', {'left': True})
                    ]
                    for parent, child, attrs in expected_edges:
                        self.assertTrue(mirrored_tree.has_edge(parent, child))
                        self.assertEqual(mirrored_tree.edges[parent, child], attrs)

if __name__ == '__main__':
    import unittest
    unittest.main()
