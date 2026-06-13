#include <bits/stdc++.h>
using namespace std;
 
#pragma GCC target("popcnt")
 
using ull = unsigned long long;
 
//std::mt19937_64 rng(std::chrono::steady_clock::now().time_since_epoch().count());
 
constexpr int V = 1E9;
constexpr int MAXN=1e9;
const int mod=998244353;
 
void solve() 
{
    int n;
    cin >> n ;
    vector<string> v(n);
    for(int i=0; i<n; i++) cin>>v[i];
    int m = v[0].size();
    int B = (m + 63) / 64; 
    vector<vector<ull>> vals(n, vector<ull>(B, 0ULL));
 
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (v[i][j] == '1') {
                int b = j >> 6;          // j / 64
                int off = j & 63;        // j % 64
                vals[i][b] |= (1ULL << off);
            }
        }
    }
    // for(auto x: vals)
    // {
    //     for(auto y : x) cout<<y<<" ";
    //     cout<<endl;
    // }
    int ans = 0;
    for (int i = 0; i < n; ++i) {
        const ull *Ai = vals[i].data();
        for (int j = i + 1; j < n; ++j) {
            const ull *Aj = vals[j].data();
            int cnt = 0;
            for (int z = 0; z < B; ++z) {
                cnt += __builtin_popcountll(Ai[z] & Aj[z]);
            }
            if (cnt >= 2) ans += 1LL * cnt * (cnt - 1) / 2;
        }
    }
    cout<<ans<<endl;
}
 
int32_t main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    //auto begin = std::chrono::high_resolution_clock::now();
    //freopen("piggyback.in", "r", stdin);
    //freopen("piggyback.out", "w", stdout);
    int t=1;
    //cin >> t;
    
    while (t--) 
    {
        solve();
    }
    // auto end = std::chrono::high_resolution_clock::now();
    // auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin);
    // cerr << "Time measured: " << elapsed.count() * 1e-9 << " seconds.\n";
    return 0;
}