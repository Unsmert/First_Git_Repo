# include <vector>
# include <iostream>
# include <algorithm>

using namespace std;

int main() {
    int n, k;

    cin >> n >> k;

    vector<int> nums(n);

    int apb, apc, bpc, temp{};

    cout << "and 1 2" << endl;
    cin >> apb;

    cout << "or 1 2" << endl;
    cin >> temp;
    apb += temp;

    cout << "and 1 3" << endl;
    cin >> apc;

    cout << "or 1 3" << endl;
    cin >> temp;
    apc += temp;

    cout << "and 2 3" << endl;
    cin >> bpc;

    cout << "or 2 3" << endl;
    cin >> temp;
    bpc += temp;

    nums[0] = (apb + apc - bpc)/2;
    nums[1] = apb - nums[0];
    nums[2] = apc - nums[0];

    for (int i = 4; i <= n; i++) {
        int zpi, temp {};

        cout << "and 1 " << i << endl;
        cin >> zpi;
        cout << "or 1 " << i << endl;
        cin >> temp;
        nums[i - 1] = zpi + temp - nums[0];
    }

    sort(nums.begin(), nums.end());

    cout << "finish " << nums[k - 1] << endl;

    return 0;
}