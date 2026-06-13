#include <cmath>
#include <iostream>
#include <vector>

using namespace std;
using ull = unsigned long long;

const ull mod = 1e9 + 7;

ull mod_inv(ull a) {
    int e = mod - 2;
    ull res = 1;
    while (e) {
        if (e & 1) res = (res * a) % mod;
        a = (a * a) % mod;
        e >>= 1;
    }
    return res;
}

int main() {
    int N, M;
    cin >> N >> M;

    int L = llround(sqrt(M));
    int K = M / (L + 1);

    vector<ull> low(L + 2, 0);
    vector<ull> high(K + 2, 0);

    ull inv_n1 = mod_inv(N - 1);

    for (int i = 1; i <= L + K; ++i) {
        int x = (i <= L) ? i : M / (L + K + 1 - i);
        ull sum = 0;

        int le = min(N, x);
        for (int l = 2, r; l <= le; l = r) {
            int q = x / l;
            r = min(N, x / q) + 1;
            ull cur = (q <= L) ? low[q] : high[M / q];
            sum = (sum + cur * (r - l)) % mod;
        }

        ull val = (sum + N) % mod * inv_n1 % mod;
        if (i <= L)
            low[i] = val;
        else
            high[L + K + 1 - i] = val;
    }

    ull ans = (M <= L) ? low[M] : high[1];
    cout << ans << "\n";

    return 0;
}