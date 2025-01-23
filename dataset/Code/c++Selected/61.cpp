class Solution {
public:
long long minimalKSum(vector<int>& nums, int k) {
int64_t result = static_cast<int64_t>(k) * (k + 1) / 2, curr = k + 1;
for (const auto& x : set<int>(cbegin(nums), cend(nums))) {
if (x < curr) {
result += curr++ - x;
}
}
return result;
}
};
