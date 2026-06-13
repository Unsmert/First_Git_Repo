# include <iostream>
# include <vector>
# include <set>
# include <algorithm>
# include <functional>
# include <string>
# include <queue>

using namespace std;

vector<pair<int, vector<int>>> initial_nodes;
vector<pair<int, vector<int>>> final_nodes;
vector<pair<bool, bool>> node_in_final;

void add_descendent_information(int node) {
    // One thing to note is that node.second = any(pair.first || pair.second per children)
    // We can recursively call this for each children before setting the value of root.second
    for (int child : initial_nodes[node].second) {
        add_descendent_information(child);
        if (!node_in_final[node].second) node_in_final[node].second = node_in_final[child].first || node_in_final[child].second; 
    }
}

void merge_nodes(int node1, int node2) {
    // given that node1 < node2
    // also given that node1.first = false
    // - combine the children of node1 and node1
    // - set value of node2.second

    cout << node1 + 1 << ' ' << node2 + 1 << '\n';

    node_in_final[node2].second |= node_in_final[node1].second;
    // vector<int>& children = (initial_nodes[node2].second.size() > initial_nodes[node1].second.size()) ? initial_nodes[node2].second : initial_nodes[node1].second;
    
    vector<int>& children = initial_nodes[node2].second;
    for (int child : initial_nodes[node1].second) {
        children.push_back(child);
        initial_nodes[child].first = node2;
    }

    vector<int>& copy = initial_nodes[initial_nodes[node1].first].second;
    for (int i = 0; i < copy.size(); ++i) {
        if (copy[i] == node1) {
            copy.erase(copy.begin() + i);
            break;
        }
    }
    initial_nodes[node1] = {};
}

void merge_all(int root) {
    if (initial_nodes[root].second.empty()) return;
    
    int maximum = -1;
    for (int child : initial_nodes[root].second) {
        maximum = max(maximum, child);
    }

    vector<int> copy = initial_nodes[root].second;
    for (int child : copy) {
        if (child != maximum) merge_nodes(child, maximum);
    }

    merge_all(maximum);
}

bool mergable(int node1, const vector<int>& node2) {
    // Assuming merge_all has been called on node1
    // Checks if we can fully destroy node1 by merging into node2
    if (node2.empty()) return false;
    if (initial_nodes[node1].second.empty()) return true;

    int child_node1 = initial_nodes[node1].second[0];

    vector<int> valid_nodes;
    for (int node: node2) {
        for (int child: initial_nodes[node].second) {
            if (child > child_node1) valid_nodes.push_back(child);
        }
    }

    return mergable(child_node1, valid_nodes);
}

pair<int, int> find_in_tree(int root, int depth) {
    int query_node {};
    for (int child : initial_nodes[root].second) {
        if (node_in_final[child].first) return {child, depth + 1};
        if (node_in_final[child].second) query_node = child;
    }
    return find_in_tree(query_node, depth + 1);
}

void solve(int root) {
    sort(initial_nodes[root].second.begin(), initial_nodes[root].second.end(), greater<int>());

    vector<int> mergable_nodes {};

    queue<int> copy;

    for (int num : initial_nodes[root].second) {
        copy.push(num);
    }

    while (!copy.empty()) {
        int node = copy.front();
        copy.pop();

        if (node_in_final[node].first) {
            mergable_nodes.push_back(node);
            continue;
        }

        if (mergable_nodes.size() == 1) {
            merge_nodes(node, mergable_nodes[0]);
            continue;
        }

        if (!(node_in_final[node].first || node_in_final[node].second)) {
            merge_all(node);
            bool flag = true;
            for (int mergable_node : mergable_nodes) {
                if (mergable_node > node && mergable(node, {mergable_node})) {
                    merge_nodes(node, mergable_node);
                    flag = false;
                    break;
                }
            }
            if (flag) copy.push(node);
            continue;
        }

        // Find tree that contains node in subtree and merge there
        // Sub problem1: Recurse tree to find a node that in final tree
        // Sub problem2: Recurse up the node in the final tree until we get to a node in mergable nodes

        pair<int, int> element = find_in_tree(node, 0);
        int mergable_node = element.first;
        int depth = element.second;
        for (int i = 0; i < depth; ++i) {
            mergable_node = final_nodes[mergable_node].first;
        }

        merge_nodes(node, mergable_node);
    }

    for (int child : initial_nodes[root].second) {
        solve(child);
    }
}

int main() {
    int T;
    cin >> T;

    for (int t = 0; t < T; t++) {
        int N;
        cin >> N;

        // Vector of nodes, with first value parent and second value children
        initial_nodes.resize(N);
        vector<bool> rootable(N, true);

        for (int i = 0; i < N - 1; i++) {
            int x, p;
            cin >> x >> p;
            --x; --p;

            rootable[x] = false;
            initial_nodes[x].first = p;
            initial_nodes[p].second.push_back(x);
        }

        int root;
        for (int i = 0; i < N; i++) {
            if (rootable[i]) {
                root = i;
                break;
            }
        }

        int M;
        cin >> M;

        final_nodes.resize(N);
        // pair.first = it is in tree, pair.second = descendant is in tree
        node_in_final.resize(N);

        for (int i = 0; i < M - 1; i++) {
            int x, p;
            cin >> x >> p;
            --x; --p;

            final_nodes[x].first = p;
            final_nodes[p].second.push_back(x);
            node_in_final[x].first = true; node_in_final[p].first = true;
        }

        add_descendent_information(root);

        cout << N - M << '\n';
        solve(root);
    }
    return 0;
}