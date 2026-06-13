// D. It's a bird! No, it's a plane! No, it's AaParsa!

# include <iostream>
# include <vector>

using namespace std;
using ll = long long;

int get_min_val(vector<bool>& visited, vector<int>& dist, int n) {
    int minimum = INT32_MAX;
    int idx;
    for (int i = 0; i < n; i++) {
        if (!visited[i] && minimum > dist[i]) {
            minimum = dist[i];
            idx = i;
        }
    }

    visited[idx] = true;
    return idx;
}

void dijkstras(vector<vector<int>>& adj_mat, vector<int>& dist, int src, int n) {
    vector<bool> visited(n, false);

    visited[src] = true;
    dist = adj_mat[src];
    dist[src] = 0;

    for (int i = 0; i < n - 1; i++) {
        int node = get_min_val(visited, dist, n);
        for (int j = 0; j < n; j++) {
            dist[j] = min(dist[j], dist[node] + adj_mat[node][((j - dist[node]) % n + n) % n]);
        }
    }
}

int main() {
    int n, m;

    cin >> n >> m;

    vector<vector<int>> adj_matrix(n, vector<int>(n, INT32_MAX - 12000));

    vector<int> cannon_starts(n);

    for (int i = 0; i < m; i++) {
        int a, b, c;

        cin >> a >> b >> c;

        adj_matrix[a][b] = min(adj_matrix[a][b], c);

        cannon_starts[a] = b;
    }

    for (int i = 0; i < n; i++) {
        int start {cannon_starts[i]};

        vector<int>& adj_arr = adj_matrix[i];

        for (int j = 0; j < 2 * n; j++) {
            int position = (j + start) % n;
            adj_arr[(position + 1) % n] = min(adj_arr[(position + 1) % n], adj_arr[position] + 1);
        }
    }

    // cout << "\n";
    // for (vector<int>& arr: adj_matrix) {
    //     for (int i: arr) {
    //         cout << i << " ";
    //     }
    //     cout << "\n";
    // }
    // cout << "\n";

    vector<vector<int>> dists(n, vector<int>(n, 0));

    for (int i = 0; i < n; i++) {
        dijkstras(adj_matrix, dists[i], i, n);
    }

    for (vector<int>& arr: dists) {
        for (int i: arr) {
            cout << i << " ";
        }
        cout << "\n";
    }

    return 0;
}