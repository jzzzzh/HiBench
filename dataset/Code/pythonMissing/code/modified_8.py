import bisect

class Solution(object):
    def findTheDistanceValue(self, arr1, arr2, d):
        result, i, j = 0, 0, 0
        for x in arr1:
            j = bisect.bisect_left(arr2, x)
            left = arr2[j-1] if j-1 >= 0 else float("-inf")
            right = arr2[j] if j < len(arr2) else float("inf")
            result += left+d < x < right-d
