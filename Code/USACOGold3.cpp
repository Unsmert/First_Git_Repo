# include <iostream>
# include <vector>
# include <deque>
# include <array>
# include <algorithm>

using namespace std;

struct dfs_helper {
    int current_node;
    vector<int> nodes_passed;
};

bool containsAll(const vector<int>& subGroup, const vector<int>& group) {
    return all_of(subGroup.begin(), subGroup.end(), [&](int element) {
        return find(group.begin(), group.end(), element) != group.end();
    });
}

void print_vec(const vector<int>& v) {
    for (size_t i = 0; i < v.size(); ++i) 
        cout << v[i] << (i == v.size() - 1 ? "" : " ");
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int T, N, M, K, L;
    
    cin >> T;
    
    for (int i = 0; i < T; i++) {
        cin >> N >> M >> K >> L;
        
        vector<int> flower_fields;
        vector<int> destination_barns;
        
        for (int j = 0; j < K; j++) {
            int flower_field;
            cin >> flower_field;
            
            flower_fields.push_back(flower_field - 1);
        }
        
        for (int j = 0; j < L; j++) {
            int destination_barn;
            cin >> destination_barn;
            
            destination_barns.push_back(destination_barn - 1);
        }
        
        vector<vector<int>> adjecency_graph(N);
        
        for (int j = 0; j < M; j++) {
            int u, v;
            cin >> u >> v;
            
            adjecency_graph[u - 1].push_back(v - 1);
            adjecency_graph[v - 1].push_back(u - 1);
        }
        
        vector<int> dist(N);
        
        deque<array<int, 2>> bfs = {{0, 0}};
        
        array<int, 2> state, adding_state;
        
        while (!bfs.empty()) {
            state = bfs.front();
            bfs.pop_front();
            
            vector<int> paths =  adjecency_graph[state[0]];
            for (const auto& path : paths) {
                if (dist[path] == 0 && path != 0) {
                    dist[path] = state[1] + 1;
                    adding_state[0] = path;
                    adding_state[1] = state[1] + 1;
                    bfs.push_back(adding_state);
                }
            }
        }
        
        for (int paths = 0; paths < N; paths++) {
            vector<int>& edges = adjecency_graph[paths];
            int start_dist = dist[paths];
            for (int path = (int)edges.size() - 1; path >= 0; path--) {
                int neighbor = edges[path];
                if (start_dist + 1 != dist[neighbor]) {
                    edges.erase(edges.begin() + path);
                }
            }
        }
        
        // Code for shortcut in test cases, but the implementation seems messy so I'll try brute forcing it
        // vector<array<int, 2>> flower_field_dist;
        // flower_field_dist.reserve(flower_fields.size());
        
        // array<int, 2> flower_field_and_dist;
        // for (const auto& flower_field : flower_fields) {
        //     flower_field_and_dist[0] = flower_field;
        //     flower_field_and_dist[1] = dist[flower_field];
        //     flower_field_dist.push_back(flower_field_and_dist);
        // }
        
        // sort(flower_field_dist.begin(), flower_field_dist.end(), [](const array<int, 2>& a, const array<int, 2>& b) { return a[1] < b[1];});
        
        // Need to confirm that for each flower_field in flower_fields, 
        // Flower_field and flower_field + 1 lie on a shortest path using flower_field_dist
        
        vector<int> possible(N - 1);
        
        deque<dfs_helper> dfs;
        dfs_helper initial_state;
        initial_state.current_node = 0;
        dfs.push_back(initial_state);
        
        dfs_helper state_ans, adding_state_ans;
        
        while (!dfs.empty()) {
            state_ans = dfs.back();
            dfs.pop_back();
            
            if (find(destination_barns.begin(), destination_barns.end(), state_ans.current_node) != destination_barns.end()) {
                
                if (containsAll(flower_fields, state_ans.nodes_passed)) {
                    
                    for (const auto& node : state_ans.nodes_passed) {
                        possible[node - 1] = 1;
                    }
                }
            }
            
            vector<int> paths =  adjecency_graph[state_ans.current_node];
            for (const auto& path : paths) {
                adding_state_ans = state_ans;
                adding_state_ans.current_node = path;
                adding_state_ans.nodes_passed.push_back(path);
                dfs.push_back(adding_state_ans);
            }
        }
        
        // cout << "Answer: \n";
        for (const auto& bit : possible) {
            cout << bit;
        }
        cout << '\n';
        // cout << "adjecency_graph: \n";
        // for (auto& row : adjecency_graph) {
        //     print_vec(row); cout << "\n"; 
        // }
        // cout << '\n';
        
        // cout << "dist: " << '\n';
        // print_vec(dist); cout << '\n';
        // cout << "flower_fields: " << '\n';
        // print_vec(flower_fields); cout << '\n';
        // // cout << "flower_field_dist" << '\n';
        // // print_vec(flower_field_dist); cout << '\n';
        // cout << "destination_barns: " << '\n';
        // print_vec(destination_barns); cout << '\n';
        
        
    }

    return 0;
}