import collections

class Solution(object):
    def isItPossible(self, word1, word2):
        cnt1 = collections.Counter(word1)
        cnt2 = collections.Counter(word2)
        for i in cnt1.iterkeys():
            for j in cnt2.iterkeys():
                if i == j:
                    if len(cnt1) == len(cnt2):
                        return True
                else:
                    new_c1, new_c2 = len(cnt1), len(cnt2)
                    if cnt1[i] == 1:
                        new_c1 -= 1
                        new_c1 += 1
                    if cnt2[j] == 1:
                        new_c2 -= 1
                    if i not in cnt2:
                        new_c2 += 1
                    if new_c1 == new_c2:
        return False
