# include <iostream>
# include <vector>
# include <array>
# include <algorithm>

using namespace std;

void push(int nodeIdx, int boundLeft, int boundRight, vector<long long>& segTree, vector<long long>& tag) {
    if (tag[nodeIdx] != 0) {
        segTree[nodeIdx] += tag[nodeIdx] * (boundRight - boundLeft + 1);
        if (boundLeft != boundRight) {
            tag[nodeIdx * 2 + 1] += tag[nodeIdx];
            tag[nodeIdx * 2 + 2] += tag[nodeIdx];
        }
        tag[nodeIdx] = 0;
    }
}

long long rquery(int nodeIdx, int boundLeft, int boundRight, int queryLeft, int queryRight, vector<long long>& segTree, vector<long long>& tag) {
    push(nodeIdx, boundLeft, boundRight, segTree, tag);

    // If the range is entirely contained outside the query, return null immediately
    if (queryRight < boundLeft || queryLeft > boundRight) {
        return 0;
    }
    // If the range is entire contained within the query, return value at node
    if (queryLeft <= boundLeft && queryRight >= boundRight) {
        return segTree[nodeIdx];
    }

    // If neither, search down both children
    int mid = (boundLeft + boundRight) / 2;
    return rquery(nodeIdx * 2 + 1, boundLeft, mid, queryLeft, queryRight, segTree, tag) + rquery(nodeIdx * 2 + 2, mid + 1, boundRight, queryLeft, queryRight, segTree, tag);
}

void rupdate(int nodeIdx, int boundLeft, int boundRight, int queryLeft, int queryRight, vector<long long>& segTree, vector<long long>& tag, long long increment) {
    push(nodeIdx, boundLeft, boundRight, segTree, tag);

    // If the range is entirely contained outside the query, return null immediately
    if (queryRight < boundLeft || queryLeft > boundRight) {
        return;
    }
    // If the range is entire contained within the query, return value at node
    if (queryLeft <= boundLeft && queryRight >= boundRight) {
        tag[nodeIdx] += increment;
        push(nodeIdx, boundLeft, boundRight, segTree, tag);
        return;
    }
    // If neither, search down both children
    int mid = (boundLeft + boundRight) / 2;
    rupdate(nodeIdx * 2 + 1, boundLeft, mid, queryLeft, queryRight, segTree, tag, increment);
    rupdate(nodeIdx * 2 + 2, mid + 1, boundRight, queryLeft, queryRight, segTree, tag, increment);

    segTree[nodeIdx] = segTree[nodeIdx * 2 + 1] + segTree[nodeIdx * 2 + 2];
}

int main() {
    int T;
    cin >> T;

    vector<long long> output;

    for (int t = 0; t < T; t++) {
        int N, C;

        cin >> N >> C;

        vector<long long> segTree(4 * N, 0);
        vector<long long> tag(4 * N, 0);

        for (int i = 0; i < C; i++) {
            int type;
            cin >> type;

            if (type) {
                int p, q;
                cin >> p >> q;

                output.push_back(rquery(0, 0, N - 1, p - 1, q - 1, segTree, tag));
            } else {
                int p, q;
                long long v;
                cin >> p >> q >> v;

                rupdate(0, 0, N - 1, p - 1, q - 1, segTree, tag, v);
            }
        }
    }

    for (long long out : output) {
        cout << out << '\n';
    }
}