# include <iostream>
# include <vector>
# include <array>
# include <algorithm>

const int INF = 1e9;

using namespace std;

struct Node {
    long long total;
    long long prefix;
    long long suffix;
    long long best;
};

Node combine(const Node& left, const Node& right) {
    if (left.best == -INF) return right;  // neutral for empty
    if (right.best == -INF) return left;

    Node res;
    res.total = left.total + right.total;
    res.prefix = max(left.prefix, left.total + right.prefix);
    res.suffix = max(right.suffix, right.total + left.suffix);
    res.best = max({left.best, right.best, left.suffix + right.prefix});
    return res;
}

Node makeLeaf(long long val) {
    Node node;
    node.total = val;
    node.prefix = val;
    node.suffix = val;
    node.best = val;
    return node;
}

void build(vector<int>& inputArr, int nodeIdx, int boundLeft, int boundRight, vector<Node>& segTree) {
    // Similar to DP: recursion with base case
    if (boundLeft == boundRight) {
        segTree[nodeIdx] = makeLeaf(inputArr[boundLeft]);
    } else {
        int mid = (boundLeft + boundRight) / 2;
        build(inputArr, nodeIdx * 2 + 1, boundLeft, mid, segTree);
        build(inputArr, nodeIdx * 2 + 2, mid + 1, boundRight, segTree);
	 // The relation (sum) below can be changed into one suitable for the problem
        segTree[nodeIdx] = combine(segTree[nodeIdx * 2 + 1], segTree[nodeIdx * 2 + 2]);
    }
}

Node query(int nodeIdx, int boundLeft, int boundRight, int queryLeft, int queryRight, vector<Node>& segTree) {
    // If the range is entirely contained outside the query, return null immediately
    if (queryRight < boundLeft || queryLeft > boundRight) {
        return makeLeaf(-INF);
    }
    // If the range is entire contained within the query, return value at node
    if (queryLeft <= boundLeft && queryRight >= boundRight) {
        return segTree[nodeIdx];
    }
    // If neither, search down both children
    int mid = (boundLeft + boundRight) / 2;
    return combine(query(nodeIdx * 2 + 1, boundLeft, mid, queryLeft, queryRight, segTree), query(nodeIdx * 2 + 2, mid + 1, boundRight, queryLeft, queryRight, segTree));
}

void update(int nodeIdx, int boundLeft, int boundRight, int pos, int newVal, vector<Node>& segTree) {
    if (boundLeft == boundRight) {
        segTree[nodeIdx] = makeLeaf(newVal);
    } else {
        int mid = (boundLeft + boundRight) / 2;
        if (pos <= mid) {
            update(nodeIdx * 2 + 1, boundLeft, mid, pos, newVal, segTree);
        } else {
            update(nodeIdx * 2 + 2, mid + 1, boundRight, pos, newVal, segTree);
        }
        segTree[nodeIdx] = combine(segTree[nodeIdx * 2 + 1], segTree[nodeIdx * 2 + 2]);
    }
}


int main() {
    int N, M;

    cin >> N;

    vector<int> arr(N);

    for (int i = 0; i < N; i++) {
        cin >> arr[i];
    }

    vector<Node> segTree(4 * N);
    
    build(arr, 0, 0, N - 1, segTree);

    vector<long long> output;

    cin >> M;

    for (int i = 0; i < M; i++) {
        int type;
        int a, b;

        cin >> type >> a >> b;

        if (type == 0) {
            update(0, 0, N - 1, a - 1, b, segTree);
            // cout << "Segment Tree after update: \n";

            // for (int a : segTree) {
            //     cout << a << ' ';
            // }
            // cout << '\n';
        } else {
            output.push_back(query(0, 0, N - 1, a - 1, b - 1, segTree).best);
        }
    }
    for (const long long& s : output) {
        cout << s << '\n';
    }
}