# include <iostream>
# include <algorithm>
# include <cstring>

using namespace std;
using ll = long long;

const ll P = 1e9 + 7;
const ll N = 305;
const ll M = 20;

ll n, A, B;
ll a[N];
ll q, l, r;
ll ansA[N][N], ansB[N][N];
ll t[M];
ll m;
ll f[M][M][3];
ll g[M][M][3];

ll get(ll a, ll b) {
    if (a < b) return 0;
    if (a == b) return 1;
    return 2;
}

void add(ll &x, ll y) {
    x += y;
    if (x >= P) x -= P;
}

void init(ll x) {
    m = 0;
    while (x) {
        t[++m] = x % 10;
        x /= 10;
    }
    reverse(t + 1, t + 1 + m);
}

void solve(ll bound, ll ans[N][N]) {
    if (bound == 0) {
        for (ll i = 1; i <= n; i++)
            for (ll j = i; j <= n; j++)
                ans[i][j] = 0;
        return;
    }
    init(bound);
    for (ll i = 1; i <= n; i++) {
        memset(f, 0, sizeof f);
        for (ll j = i; j <= n; j++) {
            ll x = a[j];
            // copy f to g (skip this digit)
            memcpy(g, f, sizeof f);
            // base: start a new number using only x
            for (ll l = 1; l <= m; l++) {
                ll rel = get(x, t[l]);
                add(g[l][l][rel], 2);
            }
            // append (add to the right)
            for (ll l = 1; l <= m; l++) {
                for (ll r = m; r > l; r--) {
                    ll v0 = f[l][r-1][0];
                    ll v2 = f[l][r-1][2];
                    add(g[l][r][0], v0);
                    add(g[l][r][2], v2);
                    ll rel = get(x, t[r]);
                    add(g[l][r][rel], f[l][r-1][1]);
                }
            }
            // prepend (add to the left)
            for (ll l = m; l >= 1; l--) {
                for (ll r = m; r >= l; r--) {
                    if (l == r) continue;
                    ll sum = (f[l+1][r][0] + f[l+1][r][1] + f[l+1][r][2]) % P;
                    if (x > t[l]) {
                        add(g[l][r][2], sum);
                    } else if (x < t[l]) {
                        add(g[l][r][0], sum);
                    } else { // x == t[l]
                        for (ll rel = 0; rel < 3; rel++)
                            add(g[l][r][rel], f[l+1][r][rel]);
                    }
                }
            }
            // copy back
            memcpy(f, g, sizeof f);
            // collect answer for subarray [i, j]
            ll total = 0;
            for (ll len = 1; len < m; len++) {
                total = (total + f[1][len][0] + f[1][len][1] + f[1][len][2]) % P;
            }
            total = (total + f[1][m][0] + f[1][m][1]) % P;
            ans[i][j] = total;
        }
    }
}

int main() {
    cin >> n >> A >> B;
    A--; // we need numbers ≤ A-1
    for (ll i = 1; i <= n; i++) cin >> a[i];
    solve(B, ansB);
    solve(A, ansA);
    cin >> q;
    while (q--) {
        cin >> l >> r;
        cout << (ansB[l][r] - ansA[l][r] + P) % P << "\n";
    }
    return 0;
}