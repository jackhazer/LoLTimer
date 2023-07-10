import requests
import datetime
import urllib.parse
SPELL_TIME=285

class Timer:
    def __init__(self):
        self.timing = 0
        self.API_KEY = 'RGAPI-6cfeec1f-5659-43e7-827c-4aabc1997f6c'
        self.API_URL = 'https://tw2.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
        self.GAME_URL = 'https://tw2.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'
        self.PLAYER_ID = 'F-k4Rjj6nr1PVes8l5b9oDNEHp5LjvZwRi2wiKdUIatXFVqxUmuiK5zHSw'

    def get_time(self, timing):
        current_time = datetime.datetime.now()
        cd = int(current_time.timestamp()) - timing // 1000 + SPELL_TIME
        minutes, seconds = divmod(cd, 60)
        text = str(minutes * 100 + seconds)
        if (minutes * 100 + seconds) // 1000 < 1:
            text = '0' + text
        return text

    def get_player_id(self, name):
        name = urllib.parse.quote(name)
        API_URL = self.API_URL + name + '?api_key=' + self.API_KEY
        response = requests.get(API_URL)
        player_info = response.json()
        player_account_id = player_info.get('id')
        self.PLAYER_ID = player_account_id
        return player_account_id

    def get_game_info(self):
        GAME_URL = self.GAME_URL + self.PLAYER_ID + '?api_key=' + self.API_KEY
        try:
            spec = requests.get(GAME_URL)
            spec.raise_for_status()
            game_info = spec.json()
            timing = game_info.get("gameStartTime")
            self.timing = timing
            return timing
        except requests.exceptions.HTTPError:
            print("Player is not currently in a game or the request failed.")
            return None

    def check_all(self, clipboard):
        if self.timing == 0:
            return clipboard
        examine = clipboard.split()
        time = self.get_time(self.timing+SPELL_TIME*1000)
        for i in range(len(examine)):
            if examine[i].isdigit() and int(examine[i]) <= int(time):
                clipboard = ' '.join(examine[:i])
                clipboard = ' '+clipboard
                break
        return clipboard

    def click(self, role, clipboard):
        clipboard = self.check_all(clipboard)

        time = self.get_time(self.timing)
        if role not in clipboard:
            overlay_text = f" {time} {role}"
            clipboard = overlay_text+clipboard
        return clipboard

    def initialize(self):
        name = '房子家的房子'
        PLAYER_ID = self.get_player_id(name)
        print(PLAYER_ID)
        if PLAYER_ID is not None:
            timing = self.get_game_info()
            if timing is not None:
                print(self.get_time(timing))
        else:
            print("Player not found.")

