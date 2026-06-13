#include <iostream>
#include <vector>
#include <set>

using namespace std;

void recurse(int node, int parent, vector<vector<int>>& adj_list, vector<set<int>>& colors, vector<int>& amt, vector<int>& node_color) {
    int largest_child = -1;
    for (int child : adj_list[node]) {
        if (child == parent) continue;
        recurse(child, node, adj_list, colors, amt, node_color);
        if (largest_child == -1 || colors[child].size() > colors[largest_child].size()) {
            largest_child = child;
        }
    }
    if (largest_child != -1) {
        colors[node].swap(colors[largest_child]);   // reuse largest child's set
    }
    for (int child : adj_list[node]) {
        if (child == parent) continue;
        if (child == largest_child) continue;
        // merge smaller child's set into current node's set
        for (int c : colors[child]) {
            colors[node].insert(c);
        }
    }
    colors[node].insert(node_color[node]);   // add own color
    amt[node] = colors[node].size();
}

int main() {
    int n;
    cin >> n;

    vector<int> node_color(n);
    for (int i = 0; i < n; i++) {
        cin >> node_color[i];
    }

    vector<set<int>> colors(n);   // initially empty
    vector<vector<int>> adj_list(n);
    vector<int> amt(n);

    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        --a; --b;
        adj_list[a].push_back(b);
        adj_list[b].push_back(a);
    }

    recurse(0, -1, adj_list, colors, amt, node_color);

    for (int num : amt) {
        cout << num << ' ';
    }

    return 0;
}