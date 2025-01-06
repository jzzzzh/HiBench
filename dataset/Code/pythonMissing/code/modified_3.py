class Solution(object):
    def alphabetBoardPath(self, target):
        result = []
        for c in target:
            y1, x1 = divmod(ord(c)-ord('a'), 5)
            result.append('U' * max(y-y1, 0))
            result.append('L' * max(x-x1, 0))
            result.append('R' * max(x1-x, 0))
            result.append('!')
            x, y = x1, y1
        return "".join(result)
