import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "app_data.json")

def get_default_data():
    return {
        "players": [
            {"first": "DANIEL", "last": "PETREAN"},
            {"first": "GUEST", "last": "PLAYER"}
        ],
        "settings": {
            "game_mode": 21,
            "theme_color": "#7B2CBF"
        }
    }

def load_data():
    if not os.path.exists(DB_PATH):
        save_data(get_default_data())
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)