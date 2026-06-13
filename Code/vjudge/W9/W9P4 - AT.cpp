#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;
using ull = unsigned long long;

struct Node {
    int children[2];
    Node() {
        children[0] = children[1] = -1;
    }
};

vector<Node> trie_nodes;

int new_node() {
    trie_nodes.emplace_back();
    return trie_nodes.size() - 1;
}

void insert_trie(int root, int value) {
    int cur = root;
    for (int i = 29; i >= 0; --i) {
        int bit = (value >> i) & 1;
        if (trie_nodes[cur].children[bit] == -1) {
            trie_nodes[cur].children[bit] = new_node();
        }
        cur = trie_nodes[cur].children[bit];
    }
}

int query_trie(int root, int value) {
    int cur = root;
    int ans = 0;
    for (int i = 29; i >= 0; --i) {
        int bit = (value >> i) & 1;
        if (trie_nodes[cur].children[bit] != -1) {
            cur = trie_nodes[cur].children[bit];
        } else {
            ans |= (1 << i);
            cur = trie_nodes[cur].children[bit ^ 1];
        }
    }
    return ans;
}

ull solve(vector<int>& a, int l, int r, int bit) {
    if (r - l <= 1 || bit < 0) return 0;

    // Partition [l, r) based on current bit
    int i = l, j = r - 1;
    while (i <= j) {
        if (((a[i] >> bit) & 1) == 0) {
            i++;
        } else {
            swap(a[i], a[j]);
            j--;
        }
    }
    int mid = i; // first index with bit = 1

    if (mid == l) return solve(a, mid, r, bit - 1);
    if (mid == r) return solve(a, l, mid, bit - 1);

    // Compute minimal XOR between the two halves
    ull best = ULLONG_MAX;
    int left_size = mid - l;
    int right_size = r - mid;
    int saved_size = trie_nodes.size();

    if (left_size < right_size) {
        int root = new_node();
        for (int idx = l; idx < mid; ++idx)
            insert_trie(root, a[idx]);
        for (int idx = mid; idx < r; ++idx) {
            int val = query_trie(root, a[idx]);
            if (val < best) best = val;
        }
    } else {
        int root = new_node();
        for (int idx = mid; idx < r; ++idx)
            insert_trie(root, a[idx]);
        for (int idx = l; idx < mid; ++idx) {
            int val = query_trie(root, a[idx]);
            if (val < best) best = val;
        }
    }
    trie_nodes.resize(saved_size); // free trie nodes

    return best + solve(a, l, mid, bit - 1) + solve(a, mid, r, bit - 1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; ++i)
        cin >> arr[i];

    cout << solve(arr, 0, n, 29) << '\n';
    return 0;
}