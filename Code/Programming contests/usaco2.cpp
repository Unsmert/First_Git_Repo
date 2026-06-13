#include <iostream>
#include <vector>

using namespace std;

// First try?
// HOLY BITMANIPILATION
int main() {
    
    int N, K;
    cin >> N >> K;
    
    // Why does c++ not allow me to use N+1 here :sob:
    int moves[20][20][20] {};
    
    for (int i = 0; i < K; i++) {
        int x, y, z;
        cin >> x >> y >> z;
        moves[x - 1][y - 1][z - 1]++;
    }
    
    int num_possible_boards = 1 << N;
    // Each board can be represented with a 1 for M and 0 for O
    // This allows us to represent all possible boards with an array of size 2**N intuitively
    vector<int> scores(num_possible_boards, 0);
    
    // Loop through all cases where x, y, z are different
    for (int x = 0; x < N; x++) {
        for (int y = 0; y < N; y++) {
            if (y == x) continue;
            for (int z = 0; z < N; z++) {
                if (z == x || z == y) continue;
                int m = moves[x][y][z];
                
                // Early exit to save time/computation
                if (m == 0) continue;
                
                // Bitshift to the proper xi, yi, zi in score
                int bx = 1 << x;
                int by = 1 << y;
                int bz = 1 << z;
                
                int involved = bx | by | bz;
                int uninvolved_bits = ((1 << N) - 1) ^ involved;
                int base_case = bx;
                
                // For the case where all other bits are "O", add M
                scores[base_case] += m;
                
                // Loop through all remaining cases where x = 1 and y, z = 0
                // Algorithm: other_cases = (other_cases - 1) & uninvolved_bits
                // It's so cool, I'm so proud of myself
                // Legit crown jewel
                for (int other_cases = uninvolved_bits; other_cases > 0; other_cases = (other_cases - 1) & uninvolved_bits) {
                    int mask = base_case | other_cases;
                    scores[mask] += m;
                }
            }
        }
    }
    
    // Simple looping algorithm to find the maximum score
    int max_score = 0;
    long long count = 0;
    for (int idx = 0; idx < num_possible_boards; idx++) {
        int score = scores[idx];
        if (score > max_score) {
            max_score = score;
            count = 1;
        } else if (score == max_score) {
            count++;
        }
    }
    
    cout << max_score << " " << count << endl;
    return 0;
}