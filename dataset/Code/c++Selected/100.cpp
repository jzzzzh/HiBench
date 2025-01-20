class Solution {
public:
vector<int> maxDepthAfterSplit(string seq) {
vector<int> result(seq.length());
for (int i = 0; i < seq.length(); ++i) {
result[i] = (i & 1) ^ (seq[i] == '(');
}
return result;
}
};
