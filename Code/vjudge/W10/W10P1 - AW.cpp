# include <vector>
# include <algorithm>
# include <iostream>
# include <cmath>

using namespace std;

int blockSize;

void preprocess(vector<int>& arr, vector<vector<int>>& blocks) {
    int n = arr.size();
    blocks.clear();
    for (int i = 0; i < n; i += blockSize) {
        int end = min(i + blockSize, n);
        vector<int> block(arr.begin() + i, arr.begin() + end);
        sort(block.begin(), block.end());
        blocks.push_back(block);
    }
}

void update(int idx, int newVal, vector<int>& arr, vector<vector<int>>& blocks, int blockSize) {
    int blockNum = idx / blockSize;
    int oldVal = arr[idx];
    arr[idx] = newVal;

    // Find and remove the old value from the block
    auto& block = blocks[blockNum];
    auto it = lower_bound(block.begin(), block.end(), oldVal);
    if (it != block.end() && *it == oldVal) {
        block.erase(it);
    }

    // Insert the new value in the correct position
    auto newPos = lower_bound(block.begin(), block.end(), newVal);
    block.insert(newPos, newVal);
}

int query(int l, int r, int x, vector<int>& arr, vector<vector<int>>& blocks) {
    int res = 0;
    int leftBlock = l / blockSize;
    int rightBlock = r / blockSize;

    if (leftBlock == rightBlock) {
        for (int i = l; i <= r; i++) {
            if (arr[i] <= x) res++;
        }
        return res;
    }

    // Left partial block
    int leftEnd = (leftBlock + 1) * blockSize - 1;
    for (int i = l; i <= leftEnd; i++) {
        if (arr[i] <= x) res++;
    }

    // Full blocks
    for (int b = leftBlock + 1; b < rightBlock; b++) {
        res += upper_bound(blocks[b].begin(), blocks[b].end(), x) - blocks[b].begin();
    }

    // Right partial block
    int rightStart = rightBlock * blockSize;
    for (int i = rightStart; i <= r; i++) {
        if (arr[i] <= x) res++;
    }

    return res;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    cin >> n >> q;
    blockSize = sqrt(n);
    if (blockSize * blockSize < n) blockSize++;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    vector<vector<int>> blocks;
    preprocess(arr, blocks);

    while (q--) {
        char type;
        cin >> type;
        if (type == 'C') {
            int p, q, x;
            cin >> p >> q >> x;
            p--; q--;
            cout << query(p, q, x, arr, blocks) << "\n";
        } else { // type == 'M'
            int i, x;
            cin >> i >> x;
            i--;
            update(i, x, arr, blocks, blockSize);
        }
    }
    return 0;
}