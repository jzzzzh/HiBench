class Solution {
public:
int amountOfTime(TreeNode* root, int start) {
const auto& iter_dfs = [&]() {
int result = -1;
using RET = pair<int, int>;
RET ret = {-1, -1};
vector<tuple<int, TreeNode *, shared_ptr<RET>, shared_ptr<RET>, RET *>> stk;
stk.emplace_back(1, root, nullptr, nullptr, &ret);
while (!empty(stk)) {
auto [step, curr, left, right, ret] = stk.back(); stk.pop_back();
if (step == 1) {
if (!curr) {
continue;
}
auto left = make_shared<RET>(-1, -1), right = make_shared<RET>(-1, -1);
stk.emplace_back(2, curr, left, right, ret);
stk.emplace_back(1, curr->right, nullptr, nullptr, right.get());
stk.emplace_back(1, curr->left, nullptr, nullptr, left.get());
} else if (step == 2) {
int d = -1;
if (curr->val == start) {
d = 0;
result = max(left->first, right->first) + 1;
} else if (left->second >= 0) {
d = left->second + 1;
result = max(result, right->first + 1 + d);
} else if (right->second >= 0) {
d = right->second + 1;
result = max(result, left->first + 1 + d);
}
*ret = make_pair(max(left->first, right->first) + 1, d);  // [height, dist_to_start]
}
}
return result;
};

return iter_dfs();
}
};

