class Solution {
public:
string alienOrder(vector<string>& words) {
unordered_set<char> nodes;
unordered_map<char, unordered_set<char>> in_degree, out_degree;
queue<char> zero_in_degree_queue;
for (const auto& word : words) {
for (const auto& c : word) {
nodes.emplace(c);
}
}
for (int i = 1; i < words.size(); ++i) {
if (words[i - 1].length() > words[i].length() &&
words[i - 1].substr(0, words[i].length()) == words[i]) {
return "";
}
findEdges(words[i - 1], words[i], &in_degree, &out_degree);
}
for (const auto& node : nodes) {
if (in_degree.find(node) == in_degree.end()) {
zero_in_degree_queue.emplace(node);
}
}

string result;
while (!zero_in_degree_queue.empty()) {
const auto& precedence = zero_in_degree_queue.front();
zero_in_degree_queue.pop();
result.push_back(precedence);

if (out_degree.find(precedence) != out_degree.end()) {
for (const auto& c : out_degree[precedence]) {
in_degree[c].erase(precedence);
if (in_degree[c].empty()) {
zero_in_degree_queue.emplace(c);
}
}
out_degree.erase(precedence);
}
}

if (!out_degree.empty()) {
return "";
}

return result;
}

private:
void findEdges(const string &word1, const string &word2,
unordered_map<char, unordered_set<char>> *in_degree,
unordered_map<char, unordered_set<char>> *out_degree) {
const int len = min(word1.length(), word2.length());
for (int i = 0; i < len; ++i) {
if (word1[i] != word2[i]) {
(*in_degree)[word2[i]].emplace(word1[i]);
(*out_degree)[word1[i]].emplace(word2[i]);
break;
}
}
}
};
