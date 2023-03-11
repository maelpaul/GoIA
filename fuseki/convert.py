# importing the module
import json
 
# Opening JSON file
with open('games.json') as json_file:
    data = json.load(json_file)
#separate into two dictionnary one for black player, another for white one
black_games = []
white_games = []

play_count_mean = 0
play_count = 0 
for game in data:
    play_count += 1
    play_count_mean += len(game["moves"])
    if game["winner"] == "W":
        white_games.append(game)
    else:
        black_games.append(game)

play_count_mean = play_count_mean/play_count
print(play_count_mean)
# print(black_games)
# print(white_games)
