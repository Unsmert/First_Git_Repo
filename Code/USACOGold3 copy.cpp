# include <iostream>
# include <vector>
# include <deque>
# include <array>
# include <algorithm>

using namespace std;

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
        
        if (flower_fields.size() == 0) {
            flower_fields.push_back(0);
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
        int max_dist = 0;
        
        while (!bfs.empty()) {
            state = bfs.front();
            bfs.pop_front();
            
            if (state[1] > max_dist) {
                max_dist = state[1];
            }
            
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
    
        vector<array<int, 2>> flower_field_dist;
        flower_field_dist.reserve(flower_fields.size());
        
        bool duplicate_flowers = false;
        
        for (int field = 0; field < flower_field_dist.size() - 1; field++) {
            if (flower_field_dist[field][1] == flower_field_dist[field + 1][1]) {
                duplicate_flowers = true;
                break;
            }
        }
        
        if (duplicate_flowers) {
            cout << string(N-1, '0') << '\n';
            continue;
        }
        
        array<int, 2> flower_field_and_dist;
        for (const auto& flower_field : flower_fields) {
            flower_field_and_dist[0] = flower_field;
            flower_field_and_dist[1] = dist[flower_field];
            flower_field_dist.push_back(flower_field_and_dist);
        }
        
        sort(flower_field_dist.begin(), flower_field_dist.end(), [](const array<int, 2>& a, const array<int, 2>& b) { return a[1] < b[1];});
        
        vector<bool> check_front(N, false);
        check_front[0] = true;
        
        deque<array<int, 2>> bfs_forward = {{0, 0}};
        int flower_index = 0;
        K = flower_fields.size();
        while (!bfs_forward.empty()) {
            state = bfs_forward.front();
            bfs_forward.pop_front();
            
            if (state[1] > flower_field_dist[flower_index][1] && flower_index < K - 1) {
                flower_index++;
            }
            
            array<int, 2> field = flower_field_dist[flower_index];
            
            vector<int> paths =  adjecency_graph[state[0]];
            for (const auto& path : paths) {
                if (state[1] != field[1] || field[0] == state[0]) {
                    check_front[path] = true;
                    adding_state[0] = path;
                    adding_state[1] = state[1] + 1;
                    bfs_forward.push_back(adding_state);
                }
            }
        }
        
        vector<vector<int>> reversed_adjecency_graph(N);
        
        for(int paths = 0; paths < N; paths++) {
            for (int path: adjecency_graph[paths]) { reversed_adjecency_graph[path].push_back(paths);
            }
        }
        
        int field_dist;
        for (array<int, 2>& flower_field : flower_field_dist) {
            field_dist = flower_field[1];
            flower_field[1] = max_dist - field_dist;
        }
        
        sort(flower_field_dist.begin(), flower_field_dist.end(), [](const array<int, 2>& a, const array<int, 2>& b) { return a[1] < b[1];});
        
        deque<array<int, 2>> bfs_backward;
        array<int, 2> initial_state;
        initial_state[1] = 0;
        
        vector<bool> check_back(N, false);
        
        for (const auto& barn : destination_barns) {
            check_back[barn] = true;
            initial_state[0] = barn;
            bfs_backward.push_back(initial_state);
        }
        
        flower_index = 0;
        
        bfs_backward.pop_back();
        if (bfs_backward.empty()) {
            for (bool bit : check_back) {
                check_back[bit] = true;
            }
        }
        
        while (!bfs_backward.empty()) {
            state = bfs_backward.front();
            bfs_backward.pop_front();
            
            if (state[1] >= flower_field_dist[flower_index][1] && flower_index < K - 1) {
                flower_index++;
            }
            
            array<int, 2> field = flower_field_dist[flower_index];
            
            vector<int> paths =  reversed_adjecency_graph[state[0]];
            for (const auto& path : paths) {
                if ((state[1] != field[1] - 1 || field[0] == path) && !check_back[path]) {
                    check_back[path] = true;
                    adding_state[0] = path;
                    adding_state[1] = state[1] + 1;
                    bfs_backward.push_back(adding_state);
                }
            }
        }
        
        vector<bool> possible(N - 1, false);
        
        for (int bit = 0; bit < N - 1; bit++) {
            possible[bit] = check_front[bit + 1] && check_back[bit + 1];
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