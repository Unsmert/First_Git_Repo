# include <iostream>
# include <vector>
# include <algorithm>
# include <string>

using namespace std;

int main() {
    int T;
    cin >> T;

    vector<string> output;

    for (int t = 0; t < T; t++) {
        int N;
        cin >> N;

        vector<int> a(N), b(N);

        for (int i = 0; i < N; i++) {
            cin >> a[i];
        }

        for (int i = 0; i < N; i++) {
            cin >> b[i];
        }

        sort(a.begin(), a.end());
        sort(b.begin(), b.end(), greater<int>());

        long long sum = 0;

        for (int i = 0; i < N; i++) {
            sum += (long long) a[i] * b[i];
        }

        output.push_back(to_string(sum));
    }

    for (int t = 0; t < T; t++) {
        cout << "case #" << (t + 1) << ": " << output[t] << '\n';
    }

    return 0;
}