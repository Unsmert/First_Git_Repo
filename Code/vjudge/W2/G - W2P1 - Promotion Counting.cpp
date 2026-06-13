# include <iostream>
# include <vector>
# include <algorithm>

using namespace std;

void dfs(int u, int p, int& timer, vector<int>& tin, vector<int>& tout, vector<vector<int>>& adj) {
    tin[u] = ++timer;
    for (int v : adj[u]) {
        if (v != p) {
            dfs(v, u, timer, tin, tout, adj);
        }
    }
    tout[u] = timer;
}

void build(vector<int>& arr, int idx, int l, int r, vector<int>& seg) {
    // Similar to DP: recursion with base case
    if (l == r) {
        seg[idx] = arr[l];
    } else {
        int mid = (l + r) / 2;
        build(arr, idx * 2 + 1, l, mid, seg);
        build(arr, idx * 2 + 2, mid + 1, r, seg);
	 // The relation (sum) below can be changed into one suitable for the problem
        seg[idx] = seg[idx * 2 + 1] + seg[idx * 2 + 2];
    }
}

int rquery(int idx, int l, int r, int ql, int qr, vector<int>& seg) {
    // If the range is entirely contained outside the query, return null immediately
    if (qr < l || ql > r) {
        return 0; // or some other appropriate default value
    }
    // If the range is entire contained within the query, return value at node
    if (ql <= l && qr >= r) {
        return seg[idx];
    }
    // If neither, search down both children
    int mid = (l + r) / 2;
    return rquery(idx * 2 + 1, l, mid, ql, qr, seg) + rquery(idx * 2 + 2, mid + 1, r, ql, qr, seg);
}

void update(int nodeIdx, int boundLeft, int boundRight, int pos, int newVal, vector<int>& segTree) {
    if (boundLeft == boundRight) {
        segTree[nodeIdx] = newVal;
    } else {
        int mid = (boundLeft + boundRight) / 2;
        if (pos <= mid) {
            update(nodeIdx * 2 + 1, boundLeft, mid, pos, newVal, segTree);
        } else {
            update(nodeIdx * 2 + 2, mid + 1, boundRight, pos, newVal, segTree);
        }
        segTree[nodeIdx] = segTree[nodeIdx * 2 + 1] + segTree[nodeIdx * 2 + 2];
    }
}

int main() {
    int N;

    cin >> N;

    vector<pair<int, int>> arr(N);

    for (int i = 0; i < N; i++) {
        cin >> arr[i].first;
        arr[i].second = i;
    }

    vector<vector<int>> adj(N);

    for (int i = 1; i < N; i++) {
        int u;
        cin >> u;
        u--;
        adj[i].push_back(u);
        adj[u].push_back(i);
    }

    // sorts in descending order by value
    sort(arr.begin(), arr.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        return a.first > b.first;
    });

    vector<int> segTree(4 * N, 0);

    int timer = -1;
    vector<int> tin(N), tout(N);

    dfs(0, -1, timer, tin, tout, adj);

    vector<pair<int, int>> answer_array(N);

    for (int i = 0; i < N; i++) {
        int idx = arr[i].second;
        answer_array[idx] = {arr[i].second, rquery(0, 0, N - 1, tin[idx], tout[idx], segTree)};
        update(0, 0, N - 1, tin[idx], 1, segTree);
    }

    // Sort in descending order by answer
    sort(answer_array.begin(), answer_array.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        return a.first < b.first;
    });

    for (const pair<int, int>& p : answer_array) {
        cout << p.second << '\n';
    }

    return 0;
}