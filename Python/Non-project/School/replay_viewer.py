import json
import os
flag = True

def print_stats(stat_dict):
    keys = stat_dict.keys()
    for key in keys:
        print(f"{key}: {stat_dict[key]}")


while flag:
    replay = input("What is your file name? ")
    if os.path.exists(replay):
        with open(replay, "rt") as replay_file:
            replay_json = replay_file.read()
            replay_data = json.loads(replay_json)
            flag = False
    else:
        print("Invalid replay file name, try again")

print("Avg stats: \n")
print_stats(replay_data["replay"]["Leaderboard"][0]["stats"])

#Stats:
#Route 1: "replay", "leaderboard", [0 or 1] for player, "stats" for total/avg stats
#Route 2: "replay", "Rounds", [Round - 1], [0 or 1] for player, "stats" for individual round stats

#Gamemode:
# "Gamemode" for differentiating between tl, qp, 40ln, etc