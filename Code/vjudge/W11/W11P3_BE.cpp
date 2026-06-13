#include <fstream>
#include <vector>
#include <set>
#include <queue>
#include <numeric>

using namespace std;

struct DSU {
    vector<int> parent;
    DSU(int n) : parent(n) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }
};

int main() {
    ifstream cin("fcolor.in");
    ofstream cout("fcolor.out");

    int N, M;
    cin >> N >> M;

    vector<set<int>> out(N);
    for (int i = 0; i < M; ++i) {
        int a, b;
        cin >> a >> b;
        --a; --b;
        out[a].insert(b);
    }

    DSU dsu(N);
    queue<int> q;
    vector<bool> inQ(N, false);

    // initial queue: nodes with out-degree > 1
    for (int i = 0; i < N; ++i) {
        if (out[i].size() > 1) {
            q.push(i);
            inQ[i] = true;
        }
    }

    while (!q.empty()) {
        int u = q.front(); q.pop();
        inQ[u] = false;

        while (out[u].size() > 1) {
            auto it = out[u].begin();
            int a = *it; ++it;
            int b = *it;

            int ra = dsu.find(a);
            int rb = dsu.find(b);

            if (ra != rb) {
                // merge the two components: keep the one with larger out‑set as the new root
                if (out[ra].size() < out[rb].size()) {
                    swap(ra, rb);
                }
                // now ra will be the new root (its out‑set is larger)
                dsu.parent[rb] = ra;   // make rb point to ra
                // merge adjacency sets
                for (int v : out[rb]) out[ra].insert(v);
                out[rb].clear();
            }
            // remove a and b from out[u] and insert the (possibly merged) component
            out[u].erase(a);
            out[u].erase(b);
            out[u].insert(dsu.find(a)); // use the updated root (ra after merge)
        }

        // after the while loop, out[u] contains at most one element
        if (out[u].size() == 1) {
            int v = *out[u].begin();
            if (out[v].size() > 1 && !inQ[v]) {
                q.push(v);
                inQ[v] = true;
            }
        }
    }

    // assign colors lexicographically smallest
    vector<int> color(N, -1);
    int nextColor = 1;
    for (int i = 0; i < N; ++i) {
        int r = dsu.find(i);
        if (color[r] == -1) {
            color[r] = nextColor++;
        }
        cout << color[r] << '\n';
    }

    return 0;
}