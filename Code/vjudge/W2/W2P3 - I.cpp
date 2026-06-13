# include <iostream>
# include <vector>
# include <unordered_map>

using namespace std;
using ull = unsigned long long;

int main() {
    int n, m;
    ull k;
    cin >> n >> m >> k;

    vector<vector<ull>> matrix(n, vector<ull>(m));
    vector<vector<unordered_map<ull, ull>>> start(n, vector<unordered_map<ull, ull>>(m));
    vector<vector<unordered_map<ull, ull>>> end(n, vector<unordered_map<ull, ull>>(m));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> matrix[i][j];
        }
    }

    start[0][0] = {{matrix[0][0], 1}};
    end[n - 1][m - 1] = {{matrix[n - 1][m - 1], 1}};

    int steps = (n + m)/2 - 1;
    int other = (n + m - 2) - steps;

    for (int diag = 0; diag < steps; diag++) {
        for (int j = 0; j < min(m, diag + 1); j++) {
            int i = diag - j;
            if (i < 0 || i >= n) continue;
            if (i < n - 1) {
                unordered_map<ull, ull>& update = start[i + 1][j];
                for (const auto& pair : start[i][j]) {
                    ull new_xor = pair.first ^ matrix[i + 1][j];
                    update[new_xor] = update[new_xor] + pair.second;
                }
            }

            if (j < m - 1) {
                unordered_map<ull, ull>& update = start[i][j + 1];
                for (const auto& pair : start[i][j]) {
                    ull new_xor = pair.first ^ matrix[i][j + 1];
                    update[new_xor] = update[new_xor] + pair.second;
                }
            }

            start[i][j] = {};
        }
    }

    for (int diag = m + n - 2; diag > m + n - 2 - other; diag--) {
        for (int i = 0; i < n; i++) {
            int j = diag - i;
            if (j < 0 || j >= m) continue;

            if (i > 0) {
                unordered_map<ull, ull>& update = end[i - 1][j];
                for (const auto& pair : end[i][j]) {
                    ull new_xor = pair.first ^ matrix[i - 1][j];
                    update[new_xor] = update[new_xor] + pair.second;
                }
            }

            if (j > 0) {
                unordered_map<ull, ull>& update = end[i][j - 1];
                for (const auto& pair : end[i][j]) {
                    ull new_xor = pair.first ^ matrix[i][j - 1];
                    update[new_xor] = update[new_xor] + pair.second;
                }
            }

            end[i][j] = {};
        }
    }

    ull ans = 0;

    for (int i = 0; i < n; i++) {
        int j = steps - i;
        if (j < 0 || j >= m) continue;

        unordered_map<ull, ull>& query = end[i][j];
        for (const auto& pair : start[i][j]) {
            ull need = pair.first ^ k ^ matrix[i][j];
            if (query.find(need) != query.end()) ans += pair.second * query[need];
        }
    }

    cout << ans;

    return 0;
}