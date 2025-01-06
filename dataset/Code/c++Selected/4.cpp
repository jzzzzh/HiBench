class Solution2 {
private:
    template<typename T>
    struct VectorHash {
        size_t operator()(const std::vector<T>& v) const {
            size_t seed = 0;
            for (const auto& i : v) {
                seed ^= std::hash<T>{}(i)  + 0x9e3779b9 + (seed<<6) + (seed>>2);
            }
            return seed;
        }
    };

public:
    vector<int> beautifulPair(vector<int>& nums1, vector<int>& nums2) {
        static const int INF = numeric_limits<int>::max();
        static const int MAX_NEIGHBOR_COUNT = (8 + 2) / 2;

        vector<vector<int>> points;
        for (int i = 0; i < size(nums1); ++i) {
            points.push_back({nums1[i], nums2[i]});
        }
        vector<int> result(3, INF);
        unordered_map<vector<int>, int, VectorHash<int>> lookup;
        for (int i = size(points) - 1; i >= 0; --i) {
            if (lookup.count(points[i])) {
                result = min(result, vector<int>{0, i, lookup[points[i]]});
            }
            lookup[points[i]] = i;
        }
        if (result[0] == 0) {
            return {result[1], result[2]};
        }
        vector<int> order(size(points));
        iota(begin(order), end(order), 0);
        sort(begin(order), end(order), [&](const auto& a, const auto& b) {
            return points[a][0] < points[b][0];
        });
        const auto& dist = [&](auto a, auto b) {
            if (a > b) {
                swap(a, b);
            }
            return vector<int>{abs(points[a][0] - points[b][0]) + abs(points[a][1] - points[b][1]), a, b};
        };

        const function<void (int, int)> merge_sort = [&](int left, int right) {
            const auto& update = [&](const auto& arr, int i) {  // added
                for (int j = size(arr) - 1; j >= 0; --j) {
                    if (points[i][1] - points[arr[j]][1] > result[0]) {
                        break;
                    }
                    assert((size(arr) - 1) - j + 1 <= MAX_NEIGHBOR_COUNT);
                    result = min(result, dist(i, arr[j]));
                }
            };
            
            if (left == right) {
                return;
            }
            const int mid = left + (right - left) / 2;
            const int x = points[order[mid]][0];  // added
            merge_sort(left, mid);
            merge_sort(mid + 1, right);
            vector<int> tmp, tmp_l, tmp_r;
            for (int l = left, r = mid + 1; l < mid + 1 || r < right + 1;) {
                if (r >= right + 1 || (l < mid + 1 && points[order[l]][1] <= points[order[r]][1])) {  // modified
                    update(tmp_r, order[l]);
                    if (x - points[order[l]][0] <= result[0]) {  // added
                        tmp_l.emplace_back(order[l]);
                    }
                    tmp.emplace_back(order[l++]);
                } else {
                    update(tmp_l, order[r]);
                    if (points[order[r]][0] - x <= result[0]) {  // added
                        tmp_r.emplace_back(order[r]);
                    }
                    tmp.emplace_back(order[r++]);
                }
            }
            copy(cbegin(tmp), cend(tmp), begin(order) + left);
        };
        
        merge_sort(0, size(points) - 1);
        return {result[1], result[2]};
    }
};

