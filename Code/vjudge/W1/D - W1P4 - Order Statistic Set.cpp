# include <iostream>
# include <vector>
# include <algorithm>
# include <unordered_map>

using namespace std;

int rquery(int nodeIdx, int boundLeft, int boundRight, int queryLeft, int queryRight, vector<int>& segTree) {
    // If the range is entirely contained outside the query, return null immediately
    if (queryRight < boundLeft || queryLeft > boundRight) {
        return 0; // or some other appropriate default value
    }
    // If the range is entire contained within the query, return value at node
    if (queryLeft <= boundLeft && queryRight >= boundRight) {
        return segTree[nodeIdx];
    }
    // If neither, search down both children
    int mid = (boundLeft + boundRight) / 2;
    return rquery(nodeIdx * 2 + 1, boundLeft, mid, queryLeft, queryRight, segTree) + rquery(nodeIdx * 2 + 2, mid + 1, boundRight, queryLeft, queryRight, segTree);
}

int kquery(int nodeIdx, int boundLeft, int boundRight, int& k, vector<int>& segTree) {
    if (boundLeft == boundRight) {
        return boundLeft;
    }
    int mid = (boundLeft + boundRight) / 2;
    if (segTree[nodeIdx * 2 + 1] >= k) {
        return kquery(nodeIdx * 2 + 1, boundLeft, mid, k, segTree);
    } else {
        k -= segTree[nodeIdx * 2 + 1];
        return kquery(nodeIdx * 2 + 2, mid + 1, boundRight, k, segTree);
    }
}

void update(int nodeIdx, int boundLeft, int boundRight, int pos, int newVal, vector<int>& segTree) {
    if (boundLeft == boundRight) {
        segTree[nodeIdx] = newVal;
    } else {
        int mid = (boundLeft + boundRight) / 2;
        if (pos <= mid) {
            update(nodeIdx * 2 + 1, boundLeft, mid, pos, newVal, segTree);
        } else {
            update(nodeIdx * 2 + 2, mid + 1, boundRight, pos, newVal, segTree);
        }
        segTree[nodeIdx] = segTree[nodeIdx * 2 + 1] + segTree[nodeIdx * 2 + 2];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int Q;

    cin >> Q;

    vector<pair<char, int>> queries(Q);

    vector<int> coordinateCompress(Q);

    for (int i = 0; i < Q; i++) {
        char type;
        int x;

        cin >> type >> x;

        if (type != 'K') coordinateCompress[i] = x;
        queries[i] = {type, x};
    }

    sort(coordinateCompress.begin(), coordinateCompress.end());
    coordinateCompress.erase(unique(coordinateCompress.begin(), coordinateCompress.end()), coordinateCompress.end());

    unordered_map<int, int> mp, reverse;

    for (int i = 0; i < coordinateCompress.size(); i++) {
        mp[coordinateCompress[i]] = i;
        reverse[i] = coordinateCompress[i];
    }

    for (pair<char, int>& query : queries) {
        if (query.first != 'K') query.second = mp[query.second];
    }

    vector<int> output;

    vector<int> segTree(4 * coordinateCompress.size(), 0);

    for (pair<char, int>& query : queries) {
        if (query.first == 'I') {
            update(0, 0, coordinateCompress.size() - 1, query.second, 1, segTree);
        } else if (query.first == 'D') {
            update(0, 0, coordinateCompress.size() - 1, query.second, 0, segTree);
        } else if (query.first == 'C') {
            output.push_back(rquery(0, 0, coordinateCompress.size() - 1, 0, query.second - 1, segTree));
        } else {
            int k = query.second;
            if (segTree[0] < k) {
                output.push_back(-1);
            } else {
                output.push_back(reverse[kquery(0, 0, coordinateCompress.size() - 1, k, segTree)]);
            }
        }
    }

    for (int out : output) {
        if (out == -1) {
            cout << "invalid" << '\n';
        } else {
            cout << out << '\n';
        }
    }
}