class Solution {
public:
int arrayPairSum(vector<int>& nums) {
const auto LEFT = -10000;
const auto RIGHT = 10000;
vector<int> lookup(RIGHT - LEFT + 1, 0);
for (const auto& num: nums) {
++lookup[num - LEFT];
}
auto r = 0, result = 0;
for (int i = LEFT; i <= RIGHT; ++i) {
result += (lookup[i - LEFT] + 1 - r) / 2 * i;
r = (lookup[i - LEFT] + r) % 2;
}
return result;
}
};
