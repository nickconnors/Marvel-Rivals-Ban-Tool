from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class Player:
    def __init__(self, username):
        self.username_without_spaces = username.replace(" ", "%20")
        self.username = username

    def get_career_stats(self, season=3, ranked=True):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)

        stats = {}
        try:
            driver.get(f"https://api.tracker.gg/api/v2/marvel-rivals/standard/profile/ign/{self.username_without_spaces}/segments/career?mode={'competitive' if ranked  else 'all'}&season={str(season)}")

            pre_tag = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.TAG_NAME, "pre"))
            )

            json_data = pre_tag.text

            stats = json.loads(json_data)

            driver.quit()
        except:
           driver.quit()

        return stats


    def get_best_heroes(self, season=3, ranked=True):
        stats = self.get_career_stats(season=season, ranked=ranked)

        try:
            segments = stats["data"]
        except:
            print(f"{self.username}: Private Stats or Invalid Username\n")
            return

        heroes = []    
        for seg in segments:
            if seg["type"] == "hero":
                # (hero name, win %, matches played)
                heroes.append((seg['metadata']['name'], seg['stats']['matchesWinPct']['displayValue'], seg['stats']['matchesPlayed']['displayValue']))

        # sort based on number of games played
        heroes = sorted(heroes, key=lambda x: float(x[2]), reverse=True)

        result = {
            "username": self.username,
            "heroes": []
        }

        for i, (name, win_pct, matches_played) in enumerate(heroes):
            if i < 3:
                hero_dict = {
                    "hero_name": name,
                    "win_pct": win_pct,
                    "matches_played": matches_played
                }
                result["heroes"].append(hero_dict)
            else:
                break

        return result