class Solution {
public:
string addBinary(string a, string b) {
string res;
size_t res_len = max(a.length(), b.length()) ;

size_t carry = 0;
for (int i = 0; i < res_len; ++i) {
const size_t a_bit_i = i < a.length() ? a[a.length() - 1 - i] - '0' : 0;
const size_t b_bit_i = i < b.length() ? b[b.length() - 1 - i] - '0' : 0;
size_t sum = carry + a_bit_i + b_bit_i;
carry = sum / 2;
sum %= 2;
res.push_back('0' + sum);
}
if (carry) {
res.push_back('0' + carry);
}
reverse(res.begin(), res.end());

return res;
}
};
