class Solution {
public:
vector<int> amountPainted(vector<vector<int>>& paint) {
const auto& query = [] (const auto& x, const auto& y) {
return x + y;
};
const auto& update = [] (const auto& x, const auto& y) {
return y;
};
const int max_pos = (*max_element(cbegin(paint), cend(paint),
[](const auto& x, const auto& y) { return x[1] < y[1]; }
))[1];
SegmentTree<int> st(max_pos, query, update);
vector<int> result;
for (const auto& x : paint) {
const int cnt = st.query(x[0], x[1] - 1);
st.update(x[0], x[1] - 1, 1);
result.emplace_back(st.query(x[0], x[1] - 1) - cnt);
}
return result;
}
};
