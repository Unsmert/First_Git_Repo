# include <vector>
# include <iostream>
# include <set>
# include <algorithm>

using namespace std;
using ull = unsigned long long;
using ui = unsigned int;

int main() {
    ui n, m;

    cin >> n >> m;
    
    vector<ull> adj_list(n);

    while (m--) {
        ui a, b;
        cin >> a >> b;
        adj_list[a] |= 1ULL << b;
        adj_list[b] |= 1ULL << a;
    }

    // Consider dp[n], where the n'th bit of n represents whether we include the n'th node
    // Then dp[n] = max(dp[n], dp[j where j = n with a bit turned off])
    // Default is 0
    // Precomputation is just finding all independent sets of the second half

    vector<pair<int, int>> dp(1 << (n / 2), {0, 0});

    for (ui i = 0; i < (1 << (n / 2)); i++) {
        ui children = 0;
        for (ui j = 0; (i >> j) != 0; j++) {
            if (1 & (i >> j)) children |= adj_list[j];
        }

        if ((i & children) != 0) continue;

        dp[i] = {__builtin_popcount(i), i};
    }

    for (ui i = 0; i < (1 << (n / 2)); i++) {
        for (ui j = 0; (i >> j) != 0; j++) {
            ui q = i & (~(1 << j));
            dp[i] = max(dp[i], dp[q]);
        }
    }
    
    ui maximum = 0;
    ull mi = 0;

    for (ull i = 0; i < (1 << ((n + 1) / 2)); i++) {
        ui base = n/2;
        ui q = (1 << (n / 2)) - 1;
        ull children = 0;
        for (ui node = 0; (i >> node) != 0; node++) {
            if (1 & (i >> node)) {
                children |= adj_list[node + base];
                q &= ~(adj_list[node + base]);
            }
        }

        if (((i << base) & children) != 0) continue;
        ui query = __builtin_popcountll(i) + dp[q].first;
        if (query > maximum) {
            maximum = query;
            mi = (i << base) | dp[q].second;
        }
    }

    cout << maximum << '\n';
    for (ui j = 0; (mi >> j) != 0; j++) {
        if (1 & (mi >> j)) cout << j << ' ';
    }

    return 0;
}