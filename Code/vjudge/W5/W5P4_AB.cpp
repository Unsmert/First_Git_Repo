#include <iostream>
#include <vector>

using namespace std;
using ull = unsigned long long;

const int MOD = 1e9 + 7;

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

    int N, K;
    cin >> N >> K;
    vector<int> a(K);
    for (int i = 0; i < K; ++i) cin >> a[i];

    // factorials and inverse factorials up to N
    vector<ull> fact(N + 1), inv_fact(N + 1);
    fact[0] = 1;
    for (int i = 1; i <= N; ++i) fact[i] = fact[i - 1] * i % MOD;
    inv_fact[N] = modpow(fact[N], MOD - 2);
    for (int i = N; i >= 1; --i) inv_fact[i - 1] = inv_fact[i] * i % MOD;

    auto nCr = [&](int n, int r) -> ull {
        if (r < 0 || r > n) return 0;
        return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD;
    };

    vector<ull> dp(N + 1, 0);
    dp[0] = 1;

    for (int ai : a) {
        vector<ull> ndp(N + 1, 0);
        for (int s = 0; s <= N; ++s) {
            if (dp[s] == 0) continue;
            int max_x = min(ai, N - s);
            for (int x = 0; x <= max_x; ++x) {
                // number of ways to choose x new children from the remaining N-s
                ull ways = nCr(N - s, x);
                // then, for this day, the factor C(N - x, ai - x)
                ways = ways * nCr(N - x, ai - x) % MOD;
                ndp[s + x] = (ndp[s + x] + dp[s] * ways) % MOD;
            }
        }
        dp.swap(ndp);
    }

    cout << dp[N] << '\n';

    return 0;
}