# include <vector>
# include <algorithm>
# include <fstream>

using namespace std;

void update(vector<vector<int>>& dp, int l, int r, vector<vector<vector<int>>>& best) {
    for (int k = l; k <= r; k++) {
        int left = (k > l) ? dp[l][k-1] : 0;
        int right = (k < r) ? dp[k+1][r] : 0;
        dp[l][r] = max(dp[l][r], left + right + best[k][l][r]);
    }
}

int main() {
    ifstream fin("pieaters.in");
    int N, M;

    fin >> N >> M;

    vector<vector<int>> cows(N, vector<int>(N, 0));
    // best[k][l][r] = best weight of cow in range [l, r] that eats k last
    vector<vector<vector<int>>> best(N, vector<vector<int>>(N, vector<int>(N, 0)));

    for (int i = 0; i < M; i++) {
        int w, l, r;
        fin >> w >> l >> r;
        l--; r--;
        cows[l][r] = max(cows[l][r], w);

        for (int k = l; k <= r; k++) {
            best[k][l][r] = max(best[k][l][r], w);
        }
    }

    for (int k = 0; k < N; k++) {
        for (int l = k; l >= 0; l--) {
            for (int r = k; r < N; r++) {
                if (l < k)
                    best[k][l][r] = max(best[k][l][r], best[k][l+1][r]);
                if (r > k)
                    best[k][l][r] = max(best[k][l][r], best[k][l][r-1]);
            }
        }
    }

    vector<vector<int>> dp(N, vector<int>(N, 0));

    for (int i = 0; i < N; i++) {
        dp[i][i] = cows[i][i];
    }

    for (int i = 1; i < N; i++) {
        for (int l = 0; l < N - i; l++) {
            int r = l + i;
            update(dp, l, r, best);
        }
    }

    ofstream fout("pieaters.out");
    fout << dp[0][N - 1] << endl;
}