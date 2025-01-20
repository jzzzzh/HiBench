import collections


# brute force solution with worse complexity but pass
class Solution(object):
    def findMinStep(self, board, hand):
        """
        :type board: str
        :type hand: str
        :rtype: int
        """

        def shrink(s):  # Time: O(n^2), Space: O(1)
            while True:
                i = 0
                for start in xrange(len(s)):
                    while i < len(s) and s[start] == s[i]:
                        i += 1
                    if i - start >= 3:
                        s = s[0:start] + s[i:]
                        break
                else:
                    break
            return s

        def findMinStepHelper(board, hand, lookup):
            if not board:
                return 0
            if not hand:
                return float("inf")
            if tuple(hand) in lookup[tuple(board)]:
                return lookup[tuple(board)][tuple(hand)]

            result = float("inf")
            for i in xrange(len(hand)):
                for j in xrange(len(board) + 1):
                    next_board = shrink(board[0:j] + hand[i : i + 1] + board[j:])
                    next_hand = hand[0:i] + hand[i + 1 :]
                    result = min(
                        result, findMinStepHelper(next_board, next_hand, lookup) + 1
                    )
            lookup[tuple(board)][tuple(hand)] = result
            return result

        lookup = collections.defaultdict(dict)
        board, hand = list(board), list(hand)
        result = findMinStepHelper(board, hand, lookup)
        return -1 if result == float("inf") else result
