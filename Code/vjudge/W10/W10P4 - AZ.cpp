#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

// Global variables for optimal memory layout
int BLOCK_SIZE;

struct Query {
    int l, r, id;
    // Sort queries based on Mo's Algorithm logic
    bool operator<(const Query& other) const {
        int block_own = l / BLOCK_SIZE;
        int block_other = other.l / BLOCK_SIZE;
        if (block_own != block_other) {
            return block_own < block_other;
        }
        // Optimization: Sort alternating blocks to reduce right pointer movements
        return (block_own & 1) ? (r < other.r) : (r > other.r);
    }
};

// Use a frequency map array up to max possible value of a_i (10^6)
int freq[1000005];
long long current_power = 0;

inline void add(int val) {
    current_power -= (long long)freq[val] * freq[val] * val;
    freq[val]++;
    current_power += (long long)freq[val] * freq[val] * val;
}

inline void remove(int val) {
    current_power -= (long long)freq[val] * freq[val] * val;
    freq[val]--;
    current_power += (long long)freq[val] * freq[val] * val;
}

int main() {
    // Fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, t;
    if (!(cin >> n >> t)) return 0;

    BLOCK_SIZE = max(1, (int)(n / sqrt(t))); // Balanced block size

    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    vector<Query> queries(t);
    for (int i = 0; i < t; i++) {
        cin >> queries[i].l >> queries[i].r;
        queries[i].l--; // Convert to 0-indexed
        queries[i].r--; 
        queries[i].id = i;
    }

    sort(queries.begin(), queries.end());

    vector<long long> ans(t);
    int cur_l = 0, cur_r = -1;

    for (const auto& q : queries) {
        // Expand or contract pointers to match query ranges
        while (cur_l > q.l) {
            cur_l--;
            add(a[cur_l]);
        }
        while (cur_r < q.r) {
            cur_r++;
            add(a[cur_r]);
        }
        while (cur_l < q.l) {
            remove(a[cur_l]);
            cur_l++;
        }
        while (cur_r > q.r) {
            remove(a[cur_r]);
            cur_r--;
        }
        ans[q.id] = current_power;
    }

    for (int i = 0; i < t; i++) {
        cout << ans[i] << "\n";
    }

    return 0;
}
