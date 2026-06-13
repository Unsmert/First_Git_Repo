#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <algorithm>

using namespace std;
using ll = long long;

const int N = 200005;

int n, m;
vector<int> g[N];
int deg[N];          // current degree
int rem_deg[N];      // degree at removal time
int parent[N], sz[N];
bool dead[N];        // true if the vertex has been removed
stack<int> stk;

int find(int x) {
    if (parent[x] == x) return x;
    return parent[x] = find(parent[x]);
}

void unite(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return;
    if (sz[a] < sz[b]) swap(a, b);
    parent[b] = a;
    sz[a] += sz[b];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        --u; --v;
        g[u].push_back(v);
        g[v].push_back(u);
        ++deg[u];
        ++deg[v];
    }

    // Min‑heap ordered by (degree, vertex)
    auto cmp = [](const pair<int,int>& a, const pair<int,int>& b) {
        if (a.first != b.first) return a.first > b.first;
        return a.second > b.second;
    };
    priority_queue<pair<int,int>, vector<pair<int,int>>, decltype(cmp)> pq(cmp);

    for (int i = 0; i < n; ++i) {
        pq.push({deg[i], i});
        parent[i] = i;
        sz[i] = 1;
    }

    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();

        if (dead[u]) continue;

        dead[u] = true;
        stk.push(u);
        rem_deg[u] = deg[u];

        for (int v : g[u]) {
            if (dead[v]) continue;
            --deg[v];
            pq.push({deg[v], v});
        }
    }


    ll ans = 0;

    while (!stk.empty()) {
        int u = stk.top();
        stk.pop();

        dead[u] = false; 

        for (int v : g[u]) {
            if (dead[v]) continue;
            unite(u, v);
        }
        
        ans = max(ans, (ll)sz[find(u)] * rem_deg[u]);
    }

    cout << ans << '\n';
    return 0;
}