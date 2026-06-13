# include <iostream>
# include <array>
# include <vector>
# include <queue>
# include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, C;
    cin >> N >> C;

    vector<int> f(C);
    for (int c = 0; c < C; c++) {
        cin >> f[c];
    }

    vector<int> p(N);
    for (int i = 0; i < N; i++) {
        cin >> p[i];
    }

    // priority queue per criterion, ordered by rank
    vector<priority_queue<int, vector<int>, greater<int>>> pq(C);

    for (int i = 0; i < N; i++) {
        int criteria_count;
        cin >> criteria_count;
        int criteria;
        for (int j = 0; j < criteria_count; j++) {
            cin >> criteria;
            pq[criteria - 1].push(i + 1);
        }
    }

    vector<bool> declined(N + 1, false);
    vector<bool> invited(N + 1, false);
    vector<int> invited_by(N + 1, 0);

    long long current_sum = 0;

    // Initial filling of invitations
for (int c = 0; c < C; c++) {
        int to_invite = f[c];
        while (to_invite > 0 && !pq[c].empty()) {
            int u = pq[c].top();
            pq[c].pop();
            
            if (invited[u]) {
                continue;
            }
            
            invited[u] = 1;
            invited_by[u] = c;
            current_sum += u;
            to_invite--;
        }
    }

    // Output for i = 0
    cout << current_sum << '\n';

    // Process declinations
    for (int i = 0; i < N - 1; i++) {
        int x = p[i];
        declined[x] = true;

        // If not invited, nothing changes
        if (!invited[x]) {
            cout << current_sum << '\n';
            continue;
        }

        // Remove invited contestant
        invited[x] = false;
        current_sum -= x;
        int priority = invited_by[x];
        // search at the priority queue of the criterion that invited x
        // keep popping until we find a non-declined contestant
        // if found, check if already invited
        // if not invited, invite and break
        // if already invited, update invited_by and search for the next priority queue
        while (!pq[priority].empty()) {
            int u = pq[priority].top();
            pq[priority].pop();

            // If declined, skip
            if (declined[u]) continue;

            // If already invited, update invited_by and continue searching
            if (invited[u]) {
                if (invited_by[u] > priority) {
                    swap(invited_by[u], priority);
                }
                continue;
            }

            // Invite this contestant
            invited[u] = true;
            invited_by[u] = priority;
            current_sum += u;
            break;
        }

        cout << current_sum << '\n';
    }

    return 0;
}