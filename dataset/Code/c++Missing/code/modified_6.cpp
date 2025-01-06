public:
    double calculateTax(vector<vector<int>>& brackets, int income) {
        int prev = 0;
        for (const auto& b : brackets) {
            result += max((min(b[0], income) - prev) * b[1] / 100.0, 0.0);
            prev = b[0];
        }
        return result;
    }
};
