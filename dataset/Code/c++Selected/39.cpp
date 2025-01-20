class Solution {
public:
vector<vector<int>> getAncestors(int n, vector<vector<int>>& edges) {
vector<vector<int>> adj(n);
for (const auto& e : edges) {
adj[e[0]].emplace_back(e[1]);
}
vector<vector<int>> result(n);
for (int u = 0; u < n; ++u) {
iter_dfs(adj, u, &result);
}
return result;
}

private:
void iter_dfs(const vector<vector<int>>& adj,
int i,
vector<vector<int>> *result) {

vector<bool> lookup(size(adj));
vector<int> stk = {i};
while (!empty(stk)) {
const auto u = stk.back(); stk.pop_back();
for (const auto& v: adj[u]) {
if (lookup[v]) {
continue;
}
lookup[v] = true;
stk.emplace_back(v);
(*result)[v].emplace_back(i);
}
}
}
};
