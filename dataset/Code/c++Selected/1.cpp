class Solution {
public:
vector<vector<int>> updateMatrix(vector<vector<int>>& matrix) {
for (int i = 0; i < matrix.size(); ++i) {
for (int j = 0; j < matrix[i].size(); ++j) {
if (!matrix[i][j]) {
continue;
}
matrix[i][j] = numeric_limits<int>::max();
if (i > 0 && matrix[i - 1][j] != numeric_limits<int>::max()) {
matrix[i][j] = min(matrix[i][j], matrix[i - 1][j] + 1);
}
if (j > 0 && matrix[i][j - 1] != numeric_limits<int>::max()) {
matrix[i][j] = min(matrix[i][j], matrix[i][j - 1] + 1);
}
}
}

for (int i = matrix.size() - 1; i >= 0; --i) {
for (int j = matrix[i].size() - 1; j >= 0; --j) {
if (!matrix[i][j]) {
continue;
}
if (i < matrix.size() - 1 && matrix[i + 1][j] != numeric_limits<int>::max()) {
matrix[i][j] = min(matrix[i][j], matrix[i + 1][j] + 1);
}
if (j < matrix[i].size() - 1 && matrix[i][j + 1] != numeric_limits<int>::max()) {
matrix[i][j] = min(matrix[i][j], matrix[i][j + 1] + 1);
}
}
}

return matrix;
}
};
