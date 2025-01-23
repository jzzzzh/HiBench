class Solution {
public:
int minSteps(int n) {
auto result = 0;
for (auto p = 2 ; p * p <= n; ++p) {
while (n % p == 0) {
result += p;
n /= p;
}
}
result += (n > 1) ? n : 0;
return result;
}
};