class Solution {
public:
string discountPrices(string sentence, int discount) {
const auto& format = [&](const auto& x) {
string result;
const auto& integers = to_string(stoll(x) * (100 - discount) / 100);
const auto& decimals = to_string(stoll(x) * (100 - discount) % 100);
const auto& paddings = string(2 - size(decimals), '0');
result += "$";
result += integers;
result += ".";
result += paddings;
result += decimals;
return result;
};

string result;
for (int i = 0, j = -1; i < size(sentence); i = j + 1) {
j = sentence.find(' ', i);
if (j == string::npos) {
j = size(sentence);
}
if (sentence[i] == '$' && j - (i + 1) > 0 && all_of(cbegin(sentence) + i + 1, cbegin(sentence) + j, ::isdigit)) {
result += format(sentence.substr(i + 1, j - (i + 1)));
} else {
for (int k = i; k < j; ++k) {
result.push_back(sentence[k]);
}
}
if (j != size(sentence)) {
result.push_back(' ');
}
}
return result;
}
};
