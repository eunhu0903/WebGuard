import json
from pathlib import Path
from utils.config import settings

TOKEN_PATH = Path(settings.TOKEN_DIR) / "agent_token.json"

def save_token(data: dict):
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, "w") as f:
        json.dump(data, f)

def load_token():
    try:
        with open(TOKEN_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
