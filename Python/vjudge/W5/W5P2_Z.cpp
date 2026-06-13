# include <iostream>
# include <vector>
# include <iomanip>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M, K;
    cin >> N >> M >> K;
    vector<bool> special(N, false);
    for (int i = 0; i < K; ++i) {
        int a; cin >> a;
        special[a] = true;
    }

    // Check impossibility: consecutive M special squares?
    int cnt = 0;
    for (int i = 0; i < N; ++i) {
        if (special[i]) cnt++;
        else cnt = 0;
        if (cnt >= M) {
            cout << "-1\n";
            return 0;
        }
    }

    vector<double> a(N + M + 5, 0.0), b(N + M + 5, 0.0);
    double sum_a = 0.0, sum_b = 0.0;

    for (int i = N - 1; i >= 0; --i) {
        if (special[i]) {
            a[i] = 1.0;
            b[i] = 0.0;
        } else {
            a[i] = sum_a / M;
            b[i] = 1.0 + sum_b / M;
        }
        // Update sliding window for next i-1
        sum_a += a[i];
        sum_b += b[i];
        if (i + M < N + M) { // remove the element that leaves the window
            sum_a -= a[i + M];
            sum_b -= b[i + M];
        }
    }

    double ans = b[0] / (1.0 - a[0]);
    cout << fixed << setprecision(10) << ans << '\n';

    return 0;
}