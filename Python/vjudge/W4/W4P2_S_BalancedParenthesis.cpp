# include <iostream>
# include <vector>
# include <algorithm>

using namespace std;

struct parenthesis{
    int required;
    int excess;
    int length;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    vector<parenthesis> parenthesis_pos_excess;
    vector<parenthesis> parenthesis_0_excess;
    vector<parenthesis> parenthesis_neg_excess;

    for (int p = 0; p < N; p++) {
        string s;
        cin >> s;

        int min_required = 0;
        int excess = 0;

        for (char& c : s) {
            if (c == '(') {
                excess++;
            } else {
                excess--;
                if (-excess > min_required) {
                    min_required = -excess;
                }
            }
        }

        parenthesis added = {min_required, excess, (int)s.length()};
        if (excess >= 0) {
            parenthesis_pos_excess.push_back(added);
        } else if (excess == 0) {
            parenthesis_0_excess.push_back(added);
        } else {
            parenthesis_neg_excess.push_back(added);
        }
    }

    // for (const parenthesis& p : parentheses) {
    //     cout << p.required << ' ' << p.excess << ' ' << p.length << '\n';
    // }

    sort(parenthesis_pos_excess.begin(), parenthesis_pos_excess.end(), [](const parenthesis& a, const parenthesis& b) {
        if (a.required == b.required) return a.excess > b.excess;
        return a.required < b.required;
    });

    // TODO: Figure out why ths sorting is 
    sort(parenthesis_neg_excess.begin(), parenthesis_neg_excess.end(), [](const parenthesis& a, const parenthesis& b) {
        return a.excess + a.required > b.excess + b.required;
        // if (a.required == b.required) return a.excess > b.excess;
        // return a.required > b.required;
    });

    // cout << "sorted\n";
    // for (const parenthesis& p : parentheses) {
    //     cout << p.required << ' ' << p.excess << ' ' << p.length << '\n';
    // }

    vector<int> dp(90000, -1);

    // If the parenthesis requires more than 0 parentheses, we want to add it as late as possible, so we iterate backwards
    // The dp state: dp[i] = the maximum length of a valid parentheses sequence that can be formed with i excess parentheses

    // For each parenthesis, we can either add it to the sequence or not
    // Choose to add = update dp state
    // Dp state update:
        // For each i, if parenthesis.required <= i, dp[i + excess] = max(dp[i + excess], dp[i] + length)
    // Then answer is dp[0]

    dp[0] = 0;
    int highest_excess = 0;

    for (const parenthesis& p : parenthesis_pos_excess) {
        for (int i = highest_excess; i >= p.required; i--) {
            if (dp[i] == -1) continue;
            dp[i + p.excess] = max(dp[i + p.excess], dp[i] + p.length);
            highest_excess = max(highest_excess, i + p.excess);
        }
    }

    for (const parenthesis& p : parenthesis_0_excess) {
        for (int i = p.required; i <= highest_excess; i++) {
            if (dp[i] == -1) continue;
            dp[i] += p.length;
        }
    }

    for (const parenthesis& p : parenthesis_neg_excess) {
        for (int i = p.required; i <= highest_excess; i++) {
            if (dp[i] == -1) continue;
            if (i + p.excess < 0) continue;
            dp[i + p.excess] = max(dp[i + p.excess], dp[i] + p.length);
            highest_excess = max(highest_excess, i + p.excess);
        }
    }

    cout << dp[0] << '\n';

    return 0;
}