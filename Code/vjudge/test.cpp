# include <iostream>
# include <map>

using namespace std;
using ull = unsigned long long;

const ull mod = 1e9 + 7;

ull mod_inv(ull a) {
    int e = mod - 2;
    ull res = 1;

    while (e) {
        if (e & 1) res = (res * a) % mod;
        a = (a * a) % mod;
        e >>= 1;
    }

    return res;
}

// for a/b mod 1e9 + 7 -> b * c = a mod 1e9 + 7, 
// Find a * c mod 1e9 + 7
ull fermats_little(int a, int b) {
    return (a * mod_inv(b)) % mod;
}

int main() {
    while (true) {
        ull a, b;
        cin >> a >> b;
        cout << fermats_little(a, b) << endl;
    }
}

// 76 27
// 148148152
// 703703711

// 1 3
// 333333336

// 2 3
// 666666672

// 4 3
// 333333337

// 4 9
// 444444448

// 7 9
// 777777784

// 2 9
// 222222224

// 19 9
// 111111114