# include <vector>
# include <iostream>
# include <algorithm>

using namespace std;
using ull = unsigned long long;

// Conceptual:

// pair.first = minimum time, pair.second = minimum fertilizer
vector<pair<int, ull>> dp0, dp1;

// dp[x]: x is some node, dp[x] represents optimal state for solving x
// in case T = 0:
//  -  dp[x] = minimum fertilizer for the minimum time to solve dp[x], end x
//  - - additionally, store time
//  - - in a separate fert[x], store sum of ai in subtree of x
//  - - for c1, c2, c3, ..., cn where ci is children of dp[x]:
//  - - - simply order traversal by fert[x], descending

// in Case of T = 1:
//  - dp[x].first = minimum fertilizer for the minimum time to solve dp[x], end x
//  - dp[x].second = minimum minimum fertilizer for the minimum time to solve dp[x], end lowest node

// updating dp[x].first: same method as described above
// dp[x].second: want to prio the node with lowest depth as last, as that achieves minimum time
//  - if 2 nodes have the same depth, choose one with lower fert[x]
//  - if 2 nodes have same depth + same fert[x], choose one arbitrarily
//  - order the rest by fert[x], descending

vector<int> depth;
vector<ull> fert;
// pair.first = parent, pair.second = children
vector<pair<int, vector<int>>> adj_list;

void init(int root, int cdepth) {
    depth[root] = cdepth;
    for (int child: adj_list[root].second) {
        init(child, cdepth + 1);
        fert[root] += fert[child];
        depth[root] = max(depth[root], depth[child]);
    }
}

void solve0(int root) {
    for (int child: adj_list[root].second) {
        solve0(child);
    }

    vector<int>& children_res = adj_list[root].second;
    sort(children_res.begin(), children_res.end(), [](const int a, const int b) {
        return (ull)(dp0[a].first + 2) * fert[b] < (ull)(dp0[b].first + 2) * fert[a];;
    });

    int running_time = 0;
    ull running_fert = 0;

    for (int res: children_res) {
        // Travel to node
        ++running_time;

        // Solve node
        running_fert += fert[res] * running_time + dp0[res].second;
        running_time += dp0[res].first;

        // Travel back
        ++running_time;
    }

    dp0[root] = {running_time, running_fert};
}

void solve1(int root) {
    vector<int>& children = adj_list[root].second;
    if (children.empty()) {
        dp1[root] = {0, 0};
        return;
    }

    // Recursively solve children first
    for (int child : children) {
        solve1(child);
    }

    sort(children.begin(), children.end(), [&](int a, int b) {
        return (ull)(dp0[a].first + 2) * fert[b] < (ull)(dp0[b].first + 2) * fert[a];
    });

    int m = children.size();
    vector<int> t(m);
    for (int i = 0; i < m; ++i) {
        int v = children[i];
        t[i] = dp0[v].first + 2;
    }

    // prefix sums for left part (starting at time 0 at node)
    vector<int> left_time(m + 1, 0);
    vector<ull> left_fert(m + 1, 0);
    int cur_time = 0;
    ull cur_fert = 0;
    for (int i = 0; i < m; ++i) {
        int v = children[i];
        cur_time += 1;                                  // travel to child
        cur_fert += fert[v] * cur_time + dp0[v].second;
        cur_time += dp0[v].first;                       // time inside subtree
        cur_time += 1;                                  // return to node
        left_time[i + 1] = cur_time;
        left_fert[i + 1] = cur_fert;
    }

    // suffix arrays: for a suffix starting at i, total fertilizer = S * sum_fert_suffix[i] + base_suffix[i]
    // where S is the time at node before processing the first child of the suffix
    vector<ull> suffix_fert_sum(m + 2, 0);
    vector<ull> suffix_base(m + 2, 0);
    vector<int> suffix_time_sum(m + 2, 0);
    ull sum_fert = 0;
    ull base = 0;
    int sum_t = 0;
    for (int i = m - 1; i >= 0; --i) {
        int v = children[i];
        base = base + (ull)t[i] * sum_fert + (fert[v] * 1 + dp0[v].second);
        sum_fert += fert[v];
        sum_t += t[i];
        suffix_base[i] = base;
        suffix_fert_sum[i] = sum_fert;
        suffix_time_sum[i] = sum_t;
    }

    int best_time = dp0[root].first;
    ull best_fert = dp0[root].second;

    for (int i = 0; i < m; ++i) {
        int last = children[i];
        ull total_fert = left_fert[i];                                  // left part
        total_fert += (ull)left_time[i] * suffix_fert_sum[i + 1] + suffix_base[i + 1]; // suffix part
        int time_after_suffix = left_time[i] + suffix_time_sum[i + 1];
        int start_last = time_after_suffix + 1;                         // travel to last child
        total_fert += fert[last] * start_last + dp1[last].second;
        int total_time = start_last + dp1[last].first;
        if (total_time < best_time || (total_time == best_time && total_fert < best_fert)) {
            best_time = total_time;
            best_fert = total_fert;
        }
    }

    dp1[root] = {best_time, best_fert};
}

int main() {
    int n, t;
    cin >> n >> t;

    depth.resize(n);
    fert.resize(n);
    adj_list.resize(n);
    dp0.resize(n);
    dp1.resize(n);

    adj_list[1].first = -1;

    for (int i = 1; i < n; i++) {
        int p, a;
        cin >> p >> a;
        --p;
        fert[i] = a;
        adj_list[i].first = p;
        adj_list[p].second.push_back(i);
    }

    init(0, 0);

    solve0(0);
    if (t == 1) {
        solve1(0);
        cout << dp1[0].first << ' ' << dp1[0].second;
        return 0;
    }

    cout << dp0[0].first << ' ' << dp0[0].second;
    return 0;
}