# include <iostream>
# include <map>

using namespace std;
using ull = unsigned long long;

const ull mod = 1e9 + 7;

struct state {
    int M_floor_i;
    int denom;
    int fraction;

    bool operator<(const state& other) const {
        if (M_floor_i != other.M_floor_i)
            return M_floor_i < other.M_floor_i;
        if (denom != other.denom)
            return denom < other.denom;
        return fraction < other.fraction;
    }
};

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
    int n, m;
    cin >> n >> m;

    map<state, int> states;

    states[{m, 1, 0}] = 1;
    
    ull mod_inv_n_1 = mod_inv(n - 1);
    ull ans = 0;

    while (!states.empty()) {
        state maxKey = states.rbegin()->first; 
        ull num_states = states[maxKey]; 
        states.erase(maxKey);

        ull value = maxKey.M_floor_i;
        ull denom = maxKey.denom;
        ull fraction = maxKey.fraction;

        if (value == 0) {
            int add = (fraction * num_states) % mod;
            ans = (ans + add) % mod;
            continue;
        }

        // d' = d · (numer+1) · numer^{-1} · (n-1)^{-1} (mod j)
        ull constant = ((fraction + mod_inv(denom)) * mod_inv_n_1) % mod;
        // ull constant = value * (numer + 1) % mod;
        // constant = constant * mod_inv(numer) % mod;
        // constant = constant * mod_inv_n_1 % mod;

        int i = 2;
        while (i <= n) {
            ull res = value / i;
            ull last;
            if (res == 0) {
                // All remaining i give quotient 0
                last = n;
            } else {
                last = value / res;
                if (last > n) last = n;
            }

            ull cnt = last - i + 1;
            // Largest i that gives the same quotient
            state inter = {res, denom * (n - 1) % mod, constant};
            states[inter] += num_states * cnt % mod;
            i = last + 1;
        }
    }

    cout << fermats_little(ans * n % mod, n - 1);

    return 0;
}