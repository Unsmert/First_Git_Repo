# include <iostream>
# include <vector>

using namespace std;
using ull = unsigned long long;

const int MOD = 998244353;

ull modpow(ull a, ull e) {
    ull res = 1;
    while (e) {
        if (e & 1) res = res * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ull n, m;
    int k;
    cin >> n >> m >> k;

    // Stirling numbers of the second kind
    vector<vector<int>> stir(k+1, vector<int>(k+1, 0));
    stir[0][0] = 1;
    for (int i = 1; i <= k; ++i) {
        for (int j = 1; j <= i; ++j) {
            stir[i][j] = (1LL * j * stir[i-1][j] + stir[i-1][j-1]) % MOD;
        }
    }

    // Precompute falling factorial and powers of p = 1/m
    int inv_m = modpow(m, MOD-2);
    int fall = 1;   // n^{\underline{j}}
    int pow_p = 1;  // p^j
    int ans = 0;

    for (int j = 1; j <= k; ++j) {
        fall = 1LL * fall * ((n - j + 1) % MOD) % MOD;
        pow_p = 1LL * pow_p * inv_m % MOD;
        ans = (ans + 1LL * stir[k][j] * fall % MOD * pow_p) % MOD;
    }

    cout << ans << '\n';

    return 0;
}