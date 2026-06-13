# include <iostream>
# include <vector>
# include <array>
# include <algorithm>

using namespace std;

struct Query {
    int left;
    int right;
    int k;
    int idx;
};

void build(vector<int>& inputArr, int nodeIdx, int boundLeft, int boundRight, vector<int>& segTree) {
    // Similar to DP: recursion with base case
    if (boundLeft == boundRight) {
        segTree[nodeIdx] = inputArr[boundLeft];
    } else {
        int mid = (boundLeft + boundRight) / 2;
        build(inputArr, nodeIdx * 2 + 1, boundLeft, mid, segTree);
        build(inputArr, nodeIdx * 2 + 2, mid + 1, boundRight, segTree);
	 // The relation (sum) below can be changed into one suitable for the problem
        segTree[nodeIdx] = segTree[nodeIdx * 2 + 1] + segTree[nodeIdx * 2 + 2];
    }
}

int sum(int nodeIdx, int boundLeft, int boundRight, int queryLeft, int queryRight, vector<int>& segTree) {
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
    return sum(nodeIdx * 2 + 1, boundLeft, mid, queryLeft, queryRight, segTree) + sum(nodeIdx * 2 + 2, mid + 1, boundRight, queryLeft, queryRight, segTree);
}

void update(int nodeIdx, int boundLeft, int boundRight, int pos, int newVal, vector<int>& segTree) {
    if (boundLeft == boundRight) {
        segTree[nodeIdx] += newVal;
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
    int N, Q;

    cin >> N;

    // First number is the value, second number is the original index
    // Sort in descending order by value
    vector<pair<int, int>> nums(N);

    for (int i = 0; i < N; i++) {
        cin >> nums[i].first;
        nums[i].second = i;
    }

    sort(nums.begin(), nums.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        return a.first > b.first;
    });

    cin >> Q;

    vector<Query> queries(Q);

    for (int i = 0; i < Q; i++) {
        int left, right, k;
        cin >> left >> right >> k;
        left--; right--;
        queries[i] = {left, right, k, i};
    }

    sort(queries.begin(), queries.end(), [](const Query& a, const Query& b) {
        return a.k > b.k;
    });

    vector<int> segTree(4 * N, 0);
    vector<int> output(Q);

    int numIdx = 0;
    int queryIdx = 0;

    while (queryIdx < Q) {
        if (numIdx < N && nums[numIdx].first > queries[queryIdx].k) {
            update(0, 0, N - 1, nums[numIdx].second, 1, segTree);
            numIdx++;
        } else {
            output[queries[queryIdx].idx] = sum(0, 0, N - 1, queries[queryIdx].left, queries[queryIdx].right, segTree);
            queryIdx++;
        }
    }

    for (int i : output) {
        cout << i << '\n';
    }

    return 0;
}