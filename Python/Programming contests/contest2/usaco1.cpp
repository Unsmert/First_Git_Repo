# include <string>
# include <vector>
# include <algorithm>
# include <iostream>
# include <array>

using namespace std;

int main() {
    int temp, C;

    cin >> temp >> C;

    const int T = temp;

    vector<string> ans_list;

    if (C == 0) {
        ans_list.reserve(T);
        
        for (int loops = 0; loops < T; loops++) {
            int N;
            cin >> N;

            string line1, line2;
            cin >> line1 >> line2;

            int count1 = 0, count2 = 0, count_JN = 0, count_NJ = 0;
            bool has_JJ = false;
            bool has_NN = false;
            for (int i = 0; i < N; i++) {
                char linei = line1[i];
                char linej = line2[i];
                count1 += linei == 'N';
                count2 += linej == 'N';
                count_JN += (linei == 'J' && linej == 'N');
                count_NJ += (linei == 'N' && linej == 'J');
                if (linei == 'J' && linej == 'J') {
                    has_JJ = true;
                }
                if (linei == 'N' && linej == 'N') {
                    has_NN = true;
                }
            }

            if (count1 % 2 == 1 || count2 % 2 == 1 || count1 != count2 || count_JN != count_NJ || (has_JJ && has_NN && (count_JN == 0))) {
                ans_list.push_back("NO");
                continue;
            }

            ans_list.push_back("YES");
        }
    } else {
        ans_list.reserve(T * 3);
        for (int loops = 0; loops < T; loops++) {
            int N;
            cin >> N;

            vector<array<int, 3>> JJ_pairs, JN_pairs, NJ_pairs, NN_pairs;
            
            string line1, line2;
            cin >> line1 >> line2;

            int count1 = 0, count2 = 0, count_JN = 0, count_NJ = 0;
            bool has_JJ = false, has_NN = false;
            char linei, linej;
            array<int, 3> arr;

            for (int i = 0; i < N; i++) {
                bool linei_J = line1[i] == 'J';
                bool linej_J = line2[i] == 'J';
                count1 += !linei_J;
                count2 += !linej_J;
                count_JN += (linei_J && !linej_J);
                count_NJ += (!linei_J && linej_J);
                if (linei_J && linej_J) {
                    has_JJ = true;
                }
                if (!linei_J && !linej_J) {
                    has_NN = true;
                }

                arr[0] = linei_J;
                arr[1] = linej_J;
                arr[2] = i + 1;

                // Compiler says there are some errors here?
                if (linei_J && linej_J) {
                    JJ_pairs.push_back(arr);
                } else if (linei_J && !linej_J) {
                    JN_pairs.push_back(arr);
                } else if (!linei_J && linej_J) {
                    NJ_pairs.push_back(arr);
                } else {
                    NN_pairs.push_back(arr);
                }
            }

            if (count1 % 2 == 1 || count2 % 2 == 1 || count1 != count2 || count_JN != count_NJ || (has_JJ && has_NN && (count_JN == 0))) {
                ans_list.push_back("NO");
                continue;
            }

            ans_list.push_back("YES");
            string order, belonging;

            if (JN_pairs.size() == 0) {
                if (JJ_pairs.size() > 0) {
                    for (int i = 0; i < N; i++) {
                        order += to_string(i + 1) + ' ';
                        belonging.push_back('J');
                    }
                } else {
                    char flip = 'J';
                    for (int i = 0; i < N; i++) {
                        order += to_string(i + 1) + ' ';
                        belonging.push_back(flip);
                        flip = flip == 'J' ? 'N' : 'J';
                    }
                }

                order.pop_back();

                ans_list.push_back(order);
                ans_list.push_back(belonging);
                continue;
            }

            for (auto &pair : JJ_pairs) {
                order += to_string(pair[2]) + ' ';
                belonging.push_back('J');
            }

            int element[3];
            element[0] = JN_pairs.back()[0];
            element[1] = JN_pairs.back()[1];
            element[2] = JN_pairs.back()[2];
            JN_pairs.pop_back();
            order += to_string(element[2]) + ' ';
            belonging.push_back('J');
            char flip = 'N';

            for (auto &pair : NN_pairs) {
                order += to_string(pair[2]) + ' ';
                belonging.push_back(flip);
                flip = flip == 'J' ? 'N' : 'J';
            }

            element[0] = NJ_pairs.back()[0];
            element[1] = NJ_pairs.back()[1];
            element[2] = NJ_pairs.back()[2];
            NJ_pairs.pop_back();
            order += to_string(element[2]) + ' ';
            belonging.push_back(flip);

            while (JN_pairs.size()) {
                element[0] = JN_pairs.back()[0];
                element[1] = JN_pairs.back()[1];
                element[2] = JN_pairs.back()[2];
                order += to_string(element[2]) + ' ';
                belonging.push_back(flip);
                flip = flip == 'J' ? 'N' : 'J';

                element[0] = NJ_pairs.back()[0];
                element[1] = NJ_pairs.back()[1];
                element[2] = NJ_pairs.back()[2];
                order += to_string(element[2]) + ' ';
                belonging.push_back(flip);
                JN_pairs.pop_back();
                NJ_pairs.pop_back();
            }

            order.pop_back();
            
            ans_list.push_back(order);
            ans_list.push_back(belonging);
        }
    }

    for (int idx = 0; idx < ans_list.size() - 1; idx++) {
        cout << ans_list[idx] << '\n';
    }
    cout << ans_list[ans_list.size() - 1];

    return 0;
}