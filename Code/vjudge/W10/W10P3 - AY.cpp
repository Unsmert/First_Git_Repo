#include <iostream>
#include <vector>
#include <queue>
#include <cmath>
#include <algorithm>
#include <cstring>
#include <stack>

using namespace std;

const int MAXN = 100010;
const int LOG = 17;      // 2^17 > 100000
const int INF = 1e9;

vector<int> adj[MAXN];
int depth[MAXN];
int parent[LOG][MAXN];
int dist[MAXN];          // distance to nearest red from fully processed batches
bool isRed[MAXN];
vector<int> allReds;     // all red nodes (ever added)
vector<int> buffer;      // newly added reds not yet merged into dist

// ------------------ LCA with binary lifting (iterative DFS) ------------------
void BuildSparseTable(int root, int n) {
    // iterative DFS to compute depth and first parents
    stack<pair<int, int>> stk;  // (node, parent)
    stk.push({root, 0});
    depth[root] = 0;
    parent[0][root] = 0;

    while (!stk.empty()) {
        auto [u, p] = stk.top(); stk.pop();
        for (int v : adj[u]) {
            if (v == p) continue;
            depth[v] = depth[u] + 1;
            parent[0][v] = u;
            stk.push({v, u});
        }
    }

    // build binary lifting table
    for (int k = 1; k < LOG; ++k) {
        for (int i = 1; i <= n; ++i) {
            if (parent[k-1][i] != 0)
                parent[k][i] = parent[k-1][parent[k-1][i]];
            else
                parent[k][i] = 0;
        }
    }
}

int lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v);
    int diff = depth[u] - depth[v];
    for (int k = 0; k < LOG; ++k)
        if (diff & (1 << k))
            u = parent[k][u];
    if (u == v) return u;
    for (int k = LOG-1; k >= 0; --k)
        if (parent[k][u] != parent[k][v]) {
            u = parent[k][u];
            v = parent[k][v];
        }
    return parent[0][u];
}

int distance(int u, int v) {
    int p = lca(u, v);
    return depth[u] + depth[v] - 2 * depth[p];
}

// ------------------ Multi‑source BFS from a list of sources ------------------
void multi_bfs(const vector<int>& sources) {
    queue<int> q;
    vector<bool> visited(MAXN, false);
    for (int src : sources) {
        dist[src] = 0;
        q.push(src);
        visited[src] = true;
    }
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
}

// ------------------ Main ------------------
int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    int n, m;
    cin >> n >> m;

    for (int i = 0; i < n-1; ++i) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    // initialise LCA structures
    BuildSparseTable(1, n);

    // initially node 1 is red
    allReds.push_back(1);
    buffer.push_back(1);
    isRed[1] = true;

    // first BFS to set initial distances
    multi_bfs(allReds);
    buffer.clear();          // buffer is now empty (all reds are processed)

    int block_size = (int)sqrt(m) + 1;   // typical sqrt decomposition threshold

    while (m--) {
        int type, v;
        cin >> type >> v;

        if (type == 1) {    // paint node v red
            if (!isRed[v]) {
                isRed[v] = true;
                allReds.push_back(v);
                buffer.push_back(v);

                // if buffer is full, merge it into dist by running BFS from all reds
                if ((int)buffer.size() >= block_size) {
                    multi_bfs(allReds);
                    buffer.clear();
                }
            }
        } else {            // query – minimal distance from v to any red node
            int ans = dist[v];   // distance from fully processed reds
            for (int red : buffer) {
                ans = min(ans, distance(v, red));
            }
            cout << ans << '\n';
        }
    }

    return 0;
}