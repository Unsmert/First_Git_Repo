# include <iostream>
# include <vector>
# include <unordered_map>

using namespace std;
using ull = unsigned long long;

void swap(unordered_map<ull, int>& idx_map, ull element1, ull element2) {
    int temp_idx = idx_map[element1];
    idx_map[element1] = idx_map[element2];
    idx_map[element2] = temp_idx;
}

int main() {
    int n;

    cin >> n;

    unordered_map<ull, int> element_to_index;
    vector<ull> nums(n);

    for (int i = 0; i < n; i++) {
        cin >> nums[i];
        element_to_index[nums[i]] = i;
    }

    for (ull bit = 1ULL << 59; bit != 0; bit >>= 1) {
        for (ull num : nums) {
            if (num & bit) {
                swap(element_to_index, num, num - bit);
            }
        }
    }

    vector<ull> ans(n);

    for (ull num : nums) {
        ans[element_to_index[num]] = num;
    }

    for (ull num : ans) {
        cout << num << " ";
    }

    return 0;
}