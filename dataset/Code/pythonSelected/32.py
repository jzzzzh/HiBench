# string, two pointers
class Solution(object):
    def makePalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        return sum(s[i] != s[~i] for i in xrange(len(s) // 2)) <= 2
