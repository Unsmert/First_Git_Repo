# include <iostream>
# include <vector>
# include <unordered_map>
# include <deque>
# include <algorithm>

using namespace std;

using ull = unsigned long long;

void add_bits(vector<int> &bit_arr, ull num) {
    int counter = 0;
    while (num != 0) {
        bit_arr[counter] += num & 1;
        num >>= 1;
        counter++;
    }
}

void add_nums(vector<int> &bit_arr, ull num, int node, vector<vector<int>>& adj_list) {
    int counter = 0;
    while (num != 0) {
        if ((num & 1) != 0) {
            if (bit_arr[counter] != 0) {
                int i = bit_arr[counter] - 1;
                adj_list[i].push_back(node);
                adj_list[node].push_back(i);
                bit_arr[counter] = 0;
            } else {
                bit_arr[counter] = node + 1;
            }
        }
         num >>= 1;
        counter++;
    }
}

int bfs(vector<vector<int>>& adj_list, int src, int num_nodes) {
    deque<pair<int, int>> queue;
    vector<bool> visited(num_nodes, false);
    vector<int> dist(num_nodes);

    vector<int> cycle_nodes;
    int min_dist = INT32_MAX;

    dist[src] = 0;
    visited[src] = true;

    queue.push_back({src, src});

    while (!queue.empty()) {
        // state.first is the current node
        // state.second is the parent node
        pair<int, int> state = queue.front();

        int u = state.first;
        int p = state.second;
        queue.pop_front();

        for (int v: adj_list[u]) {
            if (v != p) {
                if (visited[v]) {
                    cycle_nodes.push_back(v);
                    min_dist = min(min_dist, dist[u] + dist[v] + 1);
                } else {
                    dist[v] = dist[u] + 1;
                    visited[v] = true;
                    queue.push_back({v, u});
                }
            }
        }
    }
    
    return min_dist;
}

int main() {
    int n;

    cin >> n;

    vector<int> bits(60);

    vector<ull> numbers(n);
    
    for (int i = 0; i < n; i++) {
        ull num;
        cin >> num;
        numbers[i] = num;
        add_bits(bits, num);
    }

    // for (int const bit: bits) {
    //     cout << bit << " ";
    // }
    // cout << "\n";

    ull edges = 0;
    for (int i = 0; i < 60; i++) {
        int b = bits[i];
        if (b >= 3) {
            cout << 3;
            return 0;
        }

        edges |= ((ull)(b == 2)) << i;
    }

    vector<int> connect_edges(60);

    int num_nodes = 0;

    vector<vector<int>> adj_list(120);

    for (ull num: numbers) {
        if ((num & edges) != 0) {
            add_nums(connect_edges, num, num_nodes, adj_list);
            num_nodes++;
        }
    }

    for (vector<int>& arr: adj_list) {
        sort(arr.begin(), arr.end());
        arr.erase(unique(arr.begin(), arr.end()), arr.end());
    }

    // for (vector<int> arr: adj_list) {
    //     for (int num: arr) {
    //         cout << num << " ";
    //     }
    //     cout << "\n";
    // }

    int min_dist = INT32_MAX;

    for (int i = 0; i < num_nodes; i++) {
        min_dist = min(min_dist, bfs(adj_list, i, num_nodes));
    }

    cout << ((min_dist < INT32_MAX) ? min_dist : -1);
    return 0;
}