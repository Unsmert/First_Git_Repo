#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    int max_a = 0;
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
        if (a[i] > max_a) max_a = a[i];
    }

    vector<int> freq(max_a + 2, 0);
    for (int x : a) {
        freq[x]++;
    }

    vector<int> pref(max_a + 2, 0);
    for (int i = 1; i <= max_a; ++i) {
        pref[i] = pref[i-1] + freq[i];
    }

    long long ans = 0;

    for (int s = 1; s <= max_a; ++s) {
        int qmax = max_a / s;
        vector<int> odd_q;
        vector<int> odd_cnt;
        for (int q = 1; q <= qmax; ++q) {
            int L = q * s;
            int R = (q + 1) * s - 1;
            if (R > max_a) R = max_a;
            int cnt = pref[R] - pref[L-1];
            if (cnt % 2 == 1) {
                odd_q.push_back(q);
                odd_cnt.push_back(cnt);
                if (odd_q.size() > 2) break;
            }
        }
        if (odd_q.size() > 2) continue;
        if (odd_q.size() == 1 && odd_q[0] == 1) {
            ans += odd_cnt[0];
        } else if (odd_q.size() == 2 && odd_q[1] == odd_q[0] + 1) {
            ans += odd_cnt[1];
        }
    }

    cout << ans << endl;
    return 0;
}