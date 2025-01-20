class Solution {
public:
int arrangeCoins(int n) {
return static_cast<int>((sqrt(8.0 * n + 1) - 1) / 2);
}
};
