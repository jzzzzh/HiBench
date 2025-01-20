class Solution {
public:
int numberOfPatterns(int m, int n) {
vector<vector<int>> dp(1 << 9 , vector<int>(9, 0));
for (int i = 0; i < 9; ++i) {
dp[merge(0, i)][i] = 1;
}

int res = 0;
for (int used = 0; used < dp.size(); ++used) {
const auto number = number_of_keys(used);
if (number > n) {
continue;
}
for (int i = 0; i < 9; ++i) {
if (!contain(used, i)) {
continue;
}
if (m <= number && number <= n) {
res += dp[used][i];
}

const auto x1 = i / 3;
const auto y1 = i % 3;
for (int j = 0; j < 9; ++j) {
if (contain(used, j)) {
continue;
}
const auto x2 = j / 3;
const auto y2 = j % 3;
if (((x1 == x2 && abs(y1 - y2) == 2) ||
(y1 == y2 && abs(x1 - x2) == 2) ||
(abs(x1 - x2) == 2 && abs(y1 - y2) == 2)) &&
!contain(used, convert((x1 + x2) / 2, (y1 + y2) / 2))) {
continue;
}
dp[merge(used, j)][j] += dp[used][i];
}
}
}

return res;
}

private:
inline int merge(int i, int j) {
return i | (1 << j);
}

inline int number_of_keys(int i) {
int number = 0;
for (; i; i &= i - 1) {
++number;
}
return number;
}

inline bool contain(int i, int j) {
return i & (1 << j);
}

inline int convert(int i, int j) {
return 3 * i + j;
}
};

