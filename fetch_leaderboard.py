import json
import os
import sys
import requests
from datetime import datetime, timezone

TITLE_ID = "628e9"
CUSTOM_ID = os.environ["PLAYFAB_CUSTOM_ID"]

BASE_URL = f"https://{TITLE_ID}.playfabapi.com/Client"

# 1. Login / create the dedicated account
login = requests.post(
    f"{BASE_URL}/LoginWithCustomID",
    json={
        "TitleId": TITLE_ID,
        "CustomId": CUSTOM_ID,
        "CreateAccount": True
    },
    timeout=30
)

login.raise_for_status()
login_data = login.json()

if login_data.get("code") != 200:
    print(json.dumps(login_data, indent=2))
    sys.exit(1)

session_ticket = login_data["data"]["SessionTicket"]

# 2. Get Lurkers leaderboard
gamemodes = [
    ("Bedwars", "leaderboard-bedwars.json"),
    ("Capture The Flag", "leaderboard-ctf.json"),
    ("Team Deathmatch", "leaderboard-team-deathmatch.json")
]

for gamemode, filename in gamemodes:
    response = requests.post(
        f"{BASE_URL}/ExecuteCloudScript",
        headers={
            "Content-Type": "application/json",
            "X-Authorization": session_ticket
        },
        json={
            "FunctionName": "getLeaderboardNew2",
            "FunctionParameter": {
                "gamemode": gamemode
            },
            "RevisionSelection": "latest",
            "GeneratePlayStreamEvent": False
        },
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    if data.get("code") != 200:
        print(json.dumps(data, indent=2))
        sys.exit(1)

    result = data["data"]["FunctionResult"]

    output = {
        "game": "Lurkers.io",
        "gamemode": gamemode,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "lastUpdated": result.get("lastUpdated"),
        "cached": result.get("cached"),
        "players": result["value"]
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Updated {len(output['players'])} players for {gamemode}.")
