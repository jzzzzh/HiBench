class Solution {
public:
int numberOfAlternatingGroups(vector<int>& colors) {
static const int k = 3;

int result = 0;
for (int right = 0, left = 0, curr = 0; right < size(colors) + k - 1; ++right) {
if (right - left + 1 == k) {
result += curr == k - 1 ? 1 : 0;
curr -= colors[left] != colors[(left + 1) % size(colors)] ? 1 : 0;
++left;
}
curr += colors[right % size(colors)] != colors[(right + 1) % size(colors)] ? 1 : 0;
}
return result;
}
};
