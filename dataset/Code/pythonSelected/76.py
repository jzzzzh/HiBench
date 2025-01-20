class Solution(object):
    def wiggleSort(self, nums):
        """
        :type nums: List[int]
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        nums.sort()
        mid = (len(nums) - 1) / 2
        nums[::2], nums[1::2] = nums[mid::-1], nums[:mid:-1]
