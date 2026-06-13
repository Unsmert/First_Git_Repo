# include <vector>
# include <iostream>
# include <iomanip>

using namespace std;

using f = double;

vector<vector<int>> adj_list;
f ans = 0;
int n;

void recurse(int root, int parent, int depth) {
    ans += ((f)(1))/depth;
    for (int child: adj_list[root]) {
        if (child != parent) recurse(child, root, depth + 1);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;

    adj_list.resize(n);

    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        --a; --b;
        adj_list[a].push_back(b);
        adj_list[b].push_back(a);
    }

    recurse(0, -1, 1);

    cout << std::fixed << std::setprecision(20) << ans << std::endl;

    return 0;
}