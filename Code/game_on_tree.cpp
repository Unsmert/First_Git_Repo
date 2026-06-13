#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;

vector<int> adj[100005];
double expecVal = 0;

void calcExpec(int u, int p, int depth) {
    expecVal += 1.0 / depth;
    for (int v : adj[u]) {
        if (v != p) {
            calcExpec(v, u, depth + 1);
        }
    }
}

int main() {
    int n;
    cin >> n;
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    calcExpec(1, 0, 1);
    cout << fixed << setprecision(20) << expecVal << endl;
    return 0;
}