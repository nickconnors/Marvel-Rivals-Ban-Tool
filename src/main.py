from player import Player
import concurrent.futures
import predict
import keyboard
import pyautogui
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

temp_path = os.path.join(project_root, 'tmp')
os.makedirs(temp_path, exist_ok=True)

temp_file_path = os.path.join(temp_path, 'players.png')

print("Waitng for the 'F8' key...")
keyboard.wait('F8')
print("'F8' press detected")

pyautogui.screenshot().save(temp_file_path)

players = predict.get_players(temp_file_path)

def get_stats(username):
    player = Player(username)
    return player.get_best_heroes(season=3)

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=6, thread_name_prefix="thread") as executor:
    futures = [executor.submit(get_stats, player) for player in players]
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result: results.append(result)

for user in results:
    print(f'Username: {user["username"]}\nBest heroes:')
    
    for hero in user["heroes"]:
        print(f'{hero["hero_name"]}: {hero["win_pct"]} ({hero["matches_played"]} matches played)')

    print("")