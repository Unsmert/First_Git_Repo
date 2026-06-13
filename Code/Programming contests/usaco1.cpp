# include <iostream>
# include <string>
# include <vector>
# include <algorithm>
using namespace std;

int main() {
    int T, k, N;
    cin >> T >> k;
    
    string output, ans;

    vector<string> ans_list;
    
    if (k == 1) {
        char element;
        for (int loops = 0; loops < T; loops++) {
            cin >> N;

            cin >> output;

            // preprocess: swap O <-> M
            string preprocessed = output;
            for (char &c : preprocessed) {
                c = (c == 'O' ? 'M' : 'O');
            }

            bool flip = false;
            ans = "";
            
            for (int i = N - 1; i >= 0; i--) {
                if (flip) {
                    element = preprocessed[i];
                    if (element == 'O') {
                        flip = !flip;
                    }
                } else {
                    element = output[i];
                    if (element == 'O') {
                        flip = !flip;
                    }
                }
                ans.push_back(element);
            }

            ans_list.push_back("YES");
            reverse(ans.begin(), ans.end());
            ans_list.push_back(ans);
        }

        for (int idx = 0; idx < (2 * T) - 1; idx++) {
            cout << ans_list[idx] << '\n';
        }

        cout << ans_list[(2 * T) - 1];
    } else {
        for (int loops = 0; loops < T; loops++) {
            string tmp;
            cin >> tmp; // ignore
            cin >> tmp; // ignore
            ans_list.push_back("YES");
        }

        for (int idx = 0; idx < T - 1; idx++) {
            cout << ans_list[idx] << '\n';
        }
        cout << ans_list[T - 1];
    }

    return 0;
}
