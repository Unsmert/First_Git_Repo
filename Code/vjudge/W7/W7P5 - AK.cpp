# include <iostream>
# include <vector>
# include <queue>

using namespace std;
using ll = long long;

struct track {
    int dest;
    int weight;
    int type;
};

struct node {
    ll dist;
    int idx;
    int k1;
    int k2;

    bool operator()(node a, node b) {
        return a.dist > b.dist;
    }
};

bool op(node a, node b) {
    return a.dist > b.dist;
}

ll dijkstras(vector<vector<track>>& tracks, int N, int k1, int k2, int src, int dest) {
    const ll INF = 1e18;

    vector<vector<vector<ll>>> dist(N, vector<vector<ll>>(k1 + 1, vector<ll>(k2 + 1, INF)));
    vector<vector<vector<bool>>> visited(N, vector<vector<bool>>(k1 + 1, vector<bool>(k2 + 1, false)));

    priority_queue<node, vector<node>, node> pq;

    dist[src][0][0] = 0;

    pq.push({0, src, 0, 0});

    while (!pq.empty()) {
        node state = pq.top();
        pq.pop();

        ll d = state.dist;
        int i = state.idx;
        int K1 = state.k1;
        int K2 = state.k2;

        if (visited[i][K1][K2]) {
            continue;
        }

        visited[i][K1][K2] = true;
        for (track tr: tracks[i]) {
            int new_k1 = (tr.type == 1) ? K1 + 1 : K1;
            int new_k2 = (tr.type == 2) ? K2 + 1 : K2;

            if (new_k1 > k1 || new_k2 > k2) continue;
            if (dist[tr.dest][new_k1][new_k2] > dist[i][K1][K2] + tr.weight) {
                dist[tr.dest][new_k1][new_k2] = dist[i][K1][K2] + tr.weight;
                pq.push({dist[tr.dest][new_k1][new_k2], tr.dest, new_k1, new_k2});
            }
        }
    }

    if (dist[dest][k1][k2] == INF) {
        return -1;
    }

    return dist[dest][k1][k2];
}

int main() {
    int N, M, k1, k2;

    cin >> N >> M >> k1 >> k2;

    vector<vector<track>> adj_list(N);

    for (int i = 0; i < M; i++) {
        int U, V, X, C;

        cin >> U >> V >> X >> C;

        adj_list[--U].push_back({--V, X, C});
        adj_list[V].push_back({U, X, C});
    }

    int S, T;
    
    cin >> S >> T;

    cout << dijkstras(adj_list, N, k1, k2, --S, --T);
    return 0;
}