class Solution {
public:
int maxFrequencyScore(vector<int>& nums, long long k) {
sort(begin(nums), end(nums));
int64_t curr = 0;
int right = 0, left = 0;
for (; right < size(nums); ++right) {
curr += nums[right] - nums[(left + right) / 2];
if (!(curr <= k)) {
curr -= nums[((left + 1) + right) / 2] - nums[left++];
}
}
return right - left;
}
};
