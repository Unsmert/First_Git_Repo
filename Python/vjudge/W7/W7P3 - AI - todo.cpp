# include <vector>
# include <iostream>
# include <string>
# include <deque>
# include <algorithm>
# include <tuple>

using namespace std;
using ull = unsigned long long;
using ll = long long;
int INF = 1e9;

pair<int, vector<int>> bfs(vector<vector<pair<int, int>>>& adj_list, vector<tuple<int, int, int>>& edges, int N, int src) {
    vector<int> dists(N, 201);
    dists[src] = 0;

    for (int i = 0; i < N - 1; i++) {
        for (int u = 0; u < N; u++) {
            for (pair<int, int> edge : adj_list[u]) {
                int v = edge.first;
                if (dists[v] > dists[u] + edge.second) {
                    dists[v] = dists[u] + edge.second;
                }
            }
        }
    }

    for (int u = 0; u < N; u++) {
        for (pair<int, int> edge : adj_list[u]) {
            int v = edge.first;
            if (dists[v] > dists[u] + edge.second) {
                return {-1, {}};
            }
        }
    }

    for (auto& [i, j, b] : edges) {
        if (dists[i] == INF || dists[j] == INF) return {-1, {}};
        if (b == 1) {
            if (dists[j] != dists[i] + 1) return {-1, {}};
        } else { // b == 0
            if (abs(dists[i] - dists[j]) != 1) return {-1, {}};
        }
    }

    int minimum = *min_element(dists.begin(), dists.end());
    int maximum = *max_element(dists.begin(), dists.end());

    int score = maximum - minimum;

    return {score, dists};
}

int main() {
    int N, M;
    cin >> N >> M;

    vector<vector<pair<int, int>>> adj_graph(N, vector<pair<int, int>>());

    int i, j, b;

    vector<tuple<int, int, int>> edges(M);

    for (int e = 0; e < M; e++) {
        cin >> i >> j >> b;
        --i; --j;
        adj_graph[i].push_back({j, 1});
        if (b == 1) adj_graph[j].push_back({i, -1});
        else adj_graph[j].push_back({i, 1});

        edges[e] = {i, j, b};
    }

    int best_score = -1;
    vector<int> best_dists;

    for (int i = 0; i < N; i++) {
        pair<int, vector<int>> bfsed = bfs(adj_graph, edges, N, i);
        if (bfsed.first > best_score) {
            best_score = bfsed.first;
            best_dists = bfsed.second;
        }
    }

    if (best_score == -1) cout << "NO";
    else {
        cout << "YES" << '\n';
        cout << best_score << '\n';

        int minimum = *min_element(best_dists.begin(), best_dists.end());

        int addition = (minimum >= 0) ? 0 : -minimum;

        for (int i: best_dists) {
            cout << i + addition << ' ';
        }
    }
    return 0;
}