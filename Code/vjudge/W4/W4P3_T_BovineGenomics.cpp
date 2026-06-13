// USACO 2022 December Gold: Bribing Friends
// DP + sorting by X[i]

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
using ll = long long;

struct Friend {
    int pop;    // popularity P_i
    int cost;   // moonie cost C_i
    int rate;   // cones per discount X_i
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, A, B;
    cin >> N >> A >> B;

    vector<Friend> f(N);
    for (int i = 0; i < N; ++i) {
        cin >> f[i].pop >> f[i].cost >> f[i].rate;
    }

    // Sort by X (cones per discount) ascending – best discount per cone first
    sort(f.begin(), f.end(),
         [](const Friend &a, const Friend &b) { return a.rate < b.rate; });

    // dp_cone[i][c] = max popularity using first i friends,
    //                 spending exactly c ice cream cones, no moonies
    vector<vector<int>> dp_cone(N + 1, vector<int>(B + 1, 0));
    for (int i = 1; i <= N; ++i) {
        int full_cones = f[i-1].rate * f[i-1].cost;
        for (int c = 0; c <= B; ++c) {
            dp_cone[i][c] = dp_cone[i-1][c];                     // skip
            if (c >= full_cones) {
                dp_cone[i][c] = max(dp_cone[i][c],
                                    dp_cone[i-1][c - full_cones] + f[i-1].pop);
            }
        }
    }

    // dp_moon[i][m] = max popularity using friends i..N-1 (i is 1‑based index),
    //                 spending exactly m moonies, no cones
    vector<vector<int>> dp_moon(N + 2, vector<int>(A + 1, 0));
    for (int i = N; i >= 1; --i) {
        for (int m = 0; m <= A; ++m) {
            dp_moon[i][m] = dp_moon[i+1][m];                     // skip friend i-1
            if (m >= f[i-1].cost) {
                dp_moon[i][m] = max(dp_moon[i][m],
                                    dp_moon[i+1][m - f[i-1].cost] + f[i-1].pop);
            }
        }
    }

    // Combine
    int ans = max(dp_cone[N][B], dp_moon[1][A]);   // all cones or all moonies

    for (int i = 0; i < N; ++i) {                 // i = index of the mixed friend
        for (int j = 0; j <= f[i].cost; ++j) {   // j = moonies given to this friend
            int cones_needed = (f[i].cost - j) * f[i].rate;
            if (cones_needed > B) continue;
            int moon_left = A - j;
            if (moon_left < 0) continue;

            // prefix: friends 0..i-1, using cones only
            int best_pre = dp_cone[i][B - cones_needed];
            // suffix: friends i+1..N-1, using moonies only
            int best_suf = dp_moon[i+2][moon_left];   // i+2 because dp_moon[1] = friend 0
            ans = max(ans, best_pre + f[i].pop + best_suf);
        }
    }

    cout << ans << "\n";
    return 0;
}