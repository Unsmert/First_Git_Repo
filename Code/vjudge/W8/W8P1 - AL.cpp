# include <iostream>
# include <vector>

using namespace std;
using ull = unsigned long long;

int main() {
    int N;
    cin >> N;

    vector<pair<ull, int>> stack;

    ull maximum {};

    for (int i = 0; i < N; i++) {
        ull num;
        cin >> num;

        while (!stack.empty() && stack.back().first >= num) {
            ull element = stack.back().first;
            stack.pop_back();

            int l = (stack.empty()) ? -1 : stack.back().second;
            maximum = max(maximum, element * ((i - 1) - l));
        }

        stack.push_back({num, i});
    }

    int i = N - 1;
    while (!stack.empty()) {
        ull element = stack.back().first;
        stack.pop_back();

        int l = (stack.empty()) ? -1 : stack.back().second;
        maximum = max(maximum, element * (i - l));
    }

    cout << maximum;
    return 0;
}