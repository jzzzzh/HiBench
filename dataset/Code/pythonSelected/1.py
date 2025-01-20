class Solution(object):
    def numberOfRounds(self, startTime, finishTime):
        """
        :type startTime: str
        :type finishTime: str
        :rtype: int
        """
        h1, m1 = map(int, startTime.split(":"))
        h2, m2 = map(int, finishTime.split(":"))
        start = h1 * 60 + m1
        finish = h2 * 60 + m2
        if start > finish:
            finish += 1440
        return max(finish // 15 - (start + 15 - 1) // 15, 0)
