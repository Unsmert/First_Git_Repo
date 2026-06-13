#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;
using ull = unsigned long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    vector<string> anses(T);

    while (T--) {
        int n, k;
        cin >> n >> k;
        string a, b;
        cin >> a >> b;

        auto count_ones = [](const string& s) {
            return count(s.begin(), s.end(), '1');
        };
        
        int ones_a = count_ones(a);
        int ones_b = count_ones(b);
        int ones_c = 0;
        for (int i = 0; i < n; ++i)
            if (a[i] != b[i]) ++ones_c;   // a[i] XOR b[i] = '1'

        ull ac = (ull)ones_a * (n - ones_a);
        ull bc = (ull)ones_b * (n - ones_b);
        ull cc = (ull)ones_c * (n - ones_c);

        ull total_num = (1ULL << k) + 1; 
        ull first = (total_num + 2) / 3; 
        ull second = total_num / 3;
        ull ans = first * (ac + bc) + second * cc;

        anses.push_back(to_string(ans));
    }

    for (const string& s : anses)
        cout << s << '\n';

    return 0;
}