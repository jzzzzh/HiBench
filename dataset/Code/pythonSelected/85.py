from string import ascii_lowercase


# two-end bfs
class Solution(object):
    def ladderLength(self, beginWord, endWord, wordList):
        """
        :type beginWord: str
        :type endWord: str
        :type wordList: List[str]
        :rtype: int
        """
        words = set(wordList)
        if endWord not in words:
            return 0
        left, right = {beginWord}, {endWord}
        ladder = 2
        while left:
            words -= left
            new_left = set()
            for word in left:
                for new_word in (
                    word[:i] + c + word[i + 1 :]
                    for i in xrange(len(beginWord))
                    for c in ascii_lowercase
                ):
                    if new_word not in words:
                        continue
                    if new_word in right:
                        return ladder
                    new_left.add(new_word)
            left = new_left
            ladder += 1
            if len(left) > len(right):
                left, right = right, left
        return 0
