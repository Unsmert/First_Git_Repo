# include <vector>
# include <map>
# include <iostream>

using namespace std;
using ll = long long;

pair<ll, int> calculate_slope(int x1, int x2, vector<int>& heights) {
    // pair.first is the height difference, pair.second is the index difference
    // it is given that x2 > x1, but it doesn't really matter
    return {heights[x2] - heights[x1], x2 - x1};
}

bool compare_slopes(pair<ll, int> slope, pair<ll, int> qslope) {
    // Returns true if qslope >= slope
    // qh/qi >= h/i
    return (qslope.first * slope.second >= slope.first * qslope.second);
}

void delete_bigger(int i, int ui, map<int, int>& sm, vector<int> heights, int& seeable_pairs) {
    pair<ll, int> slope = calculate_slope(i, ui, heights);

    auto it = sm.upper_bound(ui);

    while (it != sm.end()) {
        pair<ll, int> qslope = calculate_slope(i, it->first, heights);

        if (compare_slopes(slope, qslope)) {
            break;
        }

        it = sm.erase(it);
        --seeable_pairs;
    }
}

int main() {
    int N;
    cin >> N;

    vector<int> heights(N);

    for (int i = 0; i < N; ++i) {
        cin >> heights[i];
    }

    vector<map<int, int>> seeable_mountains(N - 1, map<int, int>());

    int seeable_pairs {};

    for (int i = 0; i < N - 1; ++i) {
        map<int, int>& sm = seeable_mountains[i];
        sm[i + 1] = heights[i + 1];
        pair<ll, int> slope = calculate_slope(i, i+1, heights);
        ++seeable_pairs;

        for (int j = i + 2; j < N; j++) {
            pair<ll, int> query_slope = calculate_slope(i, j, heights);
            if (compare_slopes(slope, query_slope)) {
                slope = query_slope;
                sm[j] = heights[j];

                ++seeable_pairs;
            }
        }
    }

    int Q;
    cin >> Q;
    vector<int> ans(Q);

    for (int q = 0; q < Q; ++q) {
        int updated_idx, updated_height;
        cin >> updated_idx >> updated_height;
        --updated_idx;

        heights[updated_idx] += updated_height;

        for (int i = 0; i < updated_idx; i++) {
            map<int, int>& sm = seeable_mountains[i];
            if (sm.find(updated_idx) != sm.end()) {
                sm[updated_idx] = heights[updated_idx];

                delete_bigger(i, updated_idx, sm, heights, seeable_pairs);

            } else if (compare_slopes(calculate_slope(i, prev((sm.lower_bound(updated_idx)))->first, heights),  calculate_slope(i, updated_idx, heights))) {
                sm[updated_idx] = heights[updated_idx];
                ++seeable_pairs;
                delete_bigger(i, updated_idx, sm, heights, seeable_pairs);
            }
        }

        pair<ll, int> slope = calculate_slope(updated_idx, updated_idx+1, heights);
        map<int, int>& sm = seeable_mountains[updated_idx];

        for (int j = updated_idx + 2; j < N; j++) {
            pair<ll, int> query_slope = calculate_slope(updated_idx, j, heights);
            if (compare_slopes(slope, query_slope)) {
                slope = query_slope;
                if (sm.find(j) == sm.end()) {
                    sm[j] = heights[j];
                    ++seeable_pairs;
                }
            }
        }

        ans[q] = seeable_pairs;
    }

    for (int num : ans) {
        cout << num << '\n';
    }

    return 0;
}