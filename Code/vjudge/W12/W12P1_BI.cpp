# include <vector>
// # include <iostream>
# include <fstream>

using namespace std;
using ull = unsigned long long;

bool sim(ull x, ull n, ull k, ull m) {
    ull g = 0;
    while (k != 0) {
        ull remaining = n - g;
        ull y = (remaining)/x;

        if (y <= m) {
            g += m * k;
            k = 0;
            continue;
        }

        ull right_edge = ((remaining) / x) * x;
        ull d = remaining - right_edge;
        ull steps = d/y + 1;

        if (steps >= k) {
            g += k * y;
            k = 0;
        } else {
            g += steps * y;
            k -= steps;
        }
    }

    return g >= n;
}

bool bf_sim(ull x, ull n, ull k, ull m) {
    ull g = 0;
    while (k--) {
        ull y = (n - g)/x;
        ull increment = max(y, m);
        g += increment;
        if (g >= n) return true;
    }
    return g >= n;
}

int main() {
    // Goal: find some upper bound on X
    // Binary search on X:
    // - Speed up sim of X by computing all the steps of Y at once

    // 30 22 1
    // 10, 11, 12, 13, 14, 15
    // 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 
    // 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

    // START TEST 1: cin individual cases for sim
    // ull n, k, m, x;
    // cin >> n >> k >> m >> x;

    // cout << sim(x, n, k, m) << '\n' << bf_sim(x, n, k, m);
    // END TEST 1

    // START TEST 2: compare bf sim to sim for all x
    // ull n, k, m;
    // cin >> n >> k >> m;
    // ull r = n/m;

    // vector<bool> qsim, bfsim;

    // for (int x = 1; x <= r; x++) {
    //     qsim.push_back(sim(x, n, k, m));
    //     bfsim.push_back(bf_sim(x, n, k, m));
    // }

    // for (bool res : qsim) {
    //     cout << res << ' ';
    // }

    // cout << '\n';

    // for (bool res : bfsim) {
    //     cout << res << ' ';
    // }
    // END TEST 2

    ifstream cin("loan.in");

    ull N, K, M;

    cin >> N >> K >> M;

    ull l = 1;
    ull r = N/M;
    ull mid = (l + r + 1)/2;

    while (l != r) {
        if (sim(mid, N, K, M)) {
            l = mid;
            mid = (l + r + 1)/2;
        } else {
            r = mid - 1;
            mid = (l + r + 1)/2;
        }
    }

    ofstream cout("loan.out");

    cout << l;

    return 0;
}