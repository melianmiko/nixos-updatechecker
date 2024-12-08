import json
from pathlib import Path

loc = Path.home() / ".config/nixos-updatechecker.json"

with open(loc, "r") as f:
    APP_CONFIG = json.load(f)
