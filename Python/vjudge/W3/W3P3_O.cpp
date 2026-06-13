#include <iostream>
#include <vector>
#include <cstring>
using namespace std;
using ull = unsigned long long;

const int MAX_DIGITS = 39; // because 3^39 > 10^18
ull pow3[MAX_DIGITS + 1];

void precompute() {
    pow3[0] = 1;
    for (int i = 1; i <= MAX_DIGITS; ++i) {
        pow3[i] = pow3[i-1] * 3;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    precompute();

    int Q;
    cin >> Q;
    while (Q--) {
        ull d, x, y;
        cin >> d >> x >> y;

        // dp[cmp][xc][yc]
        // cmp: 0 = less, 1 = equal, 2 = greater
        ull dp[3][2][2];
        memset(dp, 0, sizeof(dp));
        dp[1][0][0] = 1; // initial state: equal so far, no carries

        for (int i = 0; i < MAX_DIGITS; ++i) {
            ull dd = (d / pow3[i]) % 3;
            ull xd = (x / pow3[i]) % 3;
            ull yd = (y / pow3[i]) % 3;

            ull new_dp[3][2][2];
            memset(new_dp, 0, sizeof(new_dp));

            for (int cmp = 0; cmp < 3; ++cmp) {
                for (int xc = 0; xc < 2; ++xc) {
                    for (int yc = 0; yc < 2; ++yc) {
                        ull cur = dp[cmp][xc][yc];
                        if (cur == 0) continue;

                        for (int j = 0; j < 3; ++j) {
                            ull xs = xd + xc + j;
                            ull xd_new = xs % 3;
                            ull xc_new = xs / 3;

                            ull ys = yd + yc + j;
                            ull yd_new = ys % 3;
                            ull yc_new = ys / 3;

                            // parity condition
                            if ((xd_new & 1) != (yd_new & 1)) continue;

                            int new_cmp;
                            if (j < dd) new_cmp = 0;
                            else if (j > dd) new_cmp = 2;
                            else new_cmp = cmp;

                            new_dp[new_cmp][xc_new][yc_new] += cur;
                        }
                    }
                }
            }
            // copy back
            memcpy(dp, new_dp, sizeof(dp));
        }

        ull ans = dp[0][0][0] + dp[1][0][0];
        cout << ans << '\n';
    }

    return 0;
}