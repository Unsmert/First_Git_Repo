# include <iostream>
# include <vector>
# include <algorithm>

using namespace std;

int solve(vector<int>& a, vector<int>& b, int n) {
    int ans = 0;
    for (int bit = 30; bit >= 0; --bit) {
        int candidate = ans | (1 << bit);
        vector<int> x(n), y(n);
        for (int i = 0; i < n; ++i) {
            x[i] = a[i] & candidate;
            y[i] = (~b[i]) & candidate;
        }
        sort(x.begin(), x.end());
        sort(y.begin(), y.end());
        if (x == y) {
            ans = candidate;
        }
    }
    return ans;
}

int main() {
    int t, n;

    cin >> t;

    vector<int> ans;

    for (int i = 0; i < t; i++) {
        cin >> n;
        vector<int> a(n);
        vector<int> b(n);

        for (int j = 0; j < n; j++) {
            cin >> a[j];
        }

        for (int j = 0; j < n; j++) {
            cin >> b[j];
        }

        ans.push_back(solve(a, b, n));
    }

    for (const int num : ans) {
        cout << num << "\n";
    }

    return 0;
}