class Solution {
public:
int maxA(int N) {
if (N < 7) {
return N;
}
if (N == 10) {  // the following rule doesn't hold when N = 10
return 20;
}
auto n = N / 5 + 1;  // n3 + n4 increases one every 5 keys
auto n3 = 5 * n - N - 1;
auto n4 = n - n3;
return pow(3, n3) * pow(4, n4);
}
};

