# include <iostream>
# include <vector>
# include <string>

using namespace std;

int floyd(vector<vector<int>>& adj_mat, int N, vector<string>& ans) {
    for (int k = 0; k < N; k++) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++){
                adj_mat[i][j] = min(adj_mat[i][j], adj_mat[i][k] + adj_mat[k][j]);
            }
        }
    }

    for (int i = 0; i < N; i++) {
        if (adj_mat[i][i] < 0) {
            ans.push_back("YES");
            return 0;
        }
    }
    ans.push_back("NO");
    return 0;
}

int main() {
    int F;
    cin >> F;

    vector<string> ans;

    for (int tests = 0; tests < F; tests++) {
        int N, M, W;
        cin >> N >> M >> W;

        vector<vector<int>> adj_mat(N, vector<int>(N, (int)1e9)); 

        for (int i = 0; i < N; i++) {
            adj_mat[i][i] = 0;
        }

        for (int i = 0; i < M; i++) {
            int a, b, c;
            cin >> a >> b >> c;
            a--;
            b--;

            adj_mat[a][b] = min(adj_mat[a][b], c);
            adj_mat[b][a] = min(adj_mat[b][a], c);
        }

        for (int i = 0; i < W; i++) {
            int a, b, c;
            cin >> a >> b >> c;
            a--;
            b--;

            adj_mat[a][b] = min(adj_mat[a][b], -c);
        }

        floyd(adj_mat, N, ans);
    }

    for (string s: ans) {
        cout << s << "\n";
    }

    return 0;
}