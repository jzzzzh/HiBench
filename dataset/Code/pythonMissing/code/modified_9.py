class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
            return root

        left, right = [self.lowestCommonAncestor(child, p, q) \
                         for child in (root.left, root.right)]
        return root if left and right else left or right
