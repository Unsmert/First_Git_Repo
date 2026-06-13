# include <iostream>
# include <vector>
# include <climits>

using namespace std;
using ull = unsigned long long;

int main() {
    int N;
    cin >> N;
   
    vector<vector<pair<ull, int>>> dp(N, vector<pair<ull, int>>(N, {0, 0}));
    for (int i = 0; i < N; i++) {
        cin >> dp[i][i].second;
    }
   
    for (int rangesize = 1; rangesize < N; rangesize++) {
        for (int i = 0; i < N - rangesize; i++) {
            int j = rangesize + i;
            ull minimum = INT64_MAX;
            int value = 0;
            for (int k = i; k < j; k++) {
                pair<ull, int> element1 = dp[i][k];
                pair<ull, int> element2 = dp[k + 1][j];
                ull query_min = element1.first + element2.first + ((ull)(element1.second ^ element2.second));
                if (query_min < minimum) {
                    minimum = query_min;
                    value = (element1.second + element2.second) % (1 << 30);
                }
            }

            dp[i][j] = {minimum, value};
        }
    }

    cout << dp[0][N - 1].first;
    return 0;
}