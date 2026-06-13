# include <vector>
# include <iostream>
# include <cmath>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;

    int o;
    cin >> o;
    vector<bool> online(n, false);
    for (int i = 0; i < o; ++i) {
        int x;
        cin >> x;
        online[--x] = true;
    }

    // initial edges
    vector<pair<int, int>> initial_edges(m);
    vector<int> deg(n, 0);
    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        --u; --v;
        initial_edges[i] = {u, v};
        ++deg[u];
        ++deg[v];
    }

    // read all queries and track degree changes to compute max degree
    struct Query {
        char type;
        int a, b;
    };
    vector<Query> queries(q);
    int add_edges = 0;
    vector<int> max_deg = deg; // start with initial degree

    for (int i = 0; i < q; ++i) {
        char type;
        cin >> type;
        if (type == 'A') {
            int u, v;
            cin >> u >> v;
            --u; --v;
            queries[i] = {'A', u, v};
            ++deg[u];
            ++deg[v];
            ++add_edges;
            if (deg[u] > max_deg[u]) max_deg[u] = deg[u];
            if (deg[v] > max_deg[v]) max_deg[v] = deg[v];
        } else if (type == 'D') {
            int u, v;
            cin >> u >> v;
            --u; --v;
            queries[i] = {'D', u, v};
            --deg[u];
            --deg[v];
        } else if (type == 'O' || type == 'F') {
            int u;
            cin >> u;
            --u;
            queries[i] = {type, u, -1};
        } else { // 'C'
            int u;
            cin >> u;
            --u;
            queries[i] = {'C', u, -1};
        }
    }

    // threshold and heavy nodes
    int total_edges_ever = m + add_edges;
    int threshold = sqrt(2 * total_edges_ever);
    if (threshold < 1) threshold = 1;

    vector<bool> is_heavy(n, false);
    for (int i = 0; i < n; ++i) {
        if (max_deg[i] >= threshold) is_heavy[i] = true;
    }

    // data structures
    vector<vector<int>> adj(n);           // neighbours for light nodes (all neighbours)
    vector<vector<int>> heavy_neigh(n);   // heavy neighbours for every node
    vector<int> heavy_online(n, 0);       // for heavy nodes: number of online neighbours

    // helper to remove a value from a vector in O(1) (swap with back and pop)
    auto remove_val = [](vector<int>& vec, int val) {
        auto it = find(vec.begin(), vec.end(), val);
        if (it != vec.end()) {
            *it = vec.back();
            vec.pop_back();
        }
    };

    // build initial graph using the heaviness classification
    for (auto& [u, v] : initial_edges) {
        if (is_heavy[u] && is_heavy[v]) {
            heavy_neigh[u].push_back(v);
            heavy_neigh[v].push_back(u);
            if (online[u]) ++heavy_online[v];
            if (online[v]) ++heavy_online[u];
        } else if (is_heavy[u]) {
            // u heavy, v light
            heavy_neigh[v].push_back(u);   // light v stores heavy neighbour u
            if (online[v]) ++heavy_online[u];
            adj[v].push_back(u);           // store in light's adjacency for queries
        } else if (is_heavy[v]) {
            heavy_neigh[u].push_back(v);
            if (online[u]) ++heavy_online[v];
            adj[u].push_back(v);
        } else {
            // both light
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    // process queries
    for (auto& qry : queries) {
        char type = qry.type;
        int u = qry.a, v = qry.b;

        if (type == 'O') { // online
            online[u] = true;
            for (int h : heavy_neigh[u]) ++heavy_online[h];
        } else if (type == 'F') { // offline
            online[u] = false;
            for (int h : heavy_neigh[u]) --heavy_online[h];
        } else if (type == 'A') { // add edge u-v
            if (is_heavy[u] && is_heavy[v]) {
                heavy_neigh[u].push_back(v);
                heavy_neigh[v].push_back(u);
                if (online[u]) ++heavy_online[v];
                if (online[v]) ++heavy_online[u];
            } else if (is_heavy[u]) {
                heavy_neigh[v].push_back(u);
                if (online[v]) ++heavy_online[u];
                adj[v].push_back(u);
            } else if (is_heavy[v]) {
                heavy_neigh[u].push_back(v);
                if (online[u]) ++heavy_online[v];
                adj[u].push_back(v);
            } else {
                adj[u].push_back(v);
                adj[v].push_back(u);
            }
        } else if (type == 'D') { // delete edge u-v
            if (is_heavy[u] && is_heavy[v]) {
                remove_val(heavy_neigh[u], v);
                remove_val(heavy_neigh[v], u);
                if (online[u]) --heavy_online[v];
                if (online[v]) --heavy_online[u];
            } else if (is_heavy[u]) {
                remove_val(heavy_neigh[v], u);
                if (online[v]) --heavy_online[u];
                remove_val(adj[v], u);
            } else if (is_heavy[v]) {
                remove_val(heavy_neigh[u], v);
                if (online[u]) --heavy_online[v];
                remove_val(adj[u], v);
            } else {
                remove_val(adj[u], v);
                remove_val(adj[v], u);
            }
        } else { // type == 'C' query
            if (is_heavy[u]) {
                cout << heavy_online[u] << '\n';
            } else {
                int cnt = 0;
                for (int w : adj[u]) if (online[w]) ++cnt;
                cout << cnt << '\n';
            }
        }
    }

    return 0;
}