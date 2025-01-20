class Solution {
public:
bool find132pattern(vector<int>& nums) {
int ak = numeric_limits<int>::min();
vector<int> stk;
for (int i = size(nums) - 1; i >= 0; --i) {
if (nums[i] < ak) {
return true;
}
while (!empty(stk) && stk.back() < nums[i]) {
ak = stk.back(), stk.pop_back();
}
stk.emplace_back(nums[i]);
}
return false;
}
};
