import json
import os
import sys
import html
import requests
from datetime import datetime, timezone

TITLE_ID = "628e9"
CUSTOM_ID = os.environ["PLAYFAB_CUSTOM_ID"]

BASE_URL = f"https://{TITLE_ID}.playfabapi.com/Client"


def generate_static_html(gamemode, players, updated_at):
    os.makedirs("data", exist_ok=True)

    filenames = {
        "Bedwars": "bedwars.html",
        "Capture The Flag": "ctf.html",
        "Team Deathmatch": "team-deathmatch.html"
    }

    filepath = os.path.join("data", filenames[gamemode])

    rows = []

    for rank, player in enumerate(players, start=1):
        player_name = player.get("Player Name", "Unknown")
        score = player.get("Score", 0)
        kills = player.get("Kills", 0)
        deaths = player.get("Deaths", 0)
        games_won = player.get("Games Won", 0)
        games_lost = player.get("Games Lost", 0)

        # K/D Ratio
        if deaths > 0:
            kd = kills / deaths
        else:
            kd = kills

        # Win Rate
        total_games = games_won + games_lost

        if total_games > 0:
            win_rate = games_won / total_games * 100
        else:
            win_rate = 0

        rows.append(f"""
        <tr>
            <td>{rank}</td>
            <td>{html.escape(str(player_name))}</td>
            <td>{score:,}</td>
            <td>{kills:,}</td>
            <td>{deaths:,}</td>
            <td>{kd:.2f}</td>
            <td>{games_won:,}</td>
            <td>{games_lost:,}</td>
            <td>{win_rate:.1f}%</td>
        </tr>
        """)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Lurkers.io - {html.escape(gamemode)} Leaderboard</title>

    <meta name="description"
          content="Lurkers.io {html.escape(gamemode)} leaderboard.">

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: white;
            color: #111;
        }}

        h1 {{
            margin-bottom: 5px;
        }}

        .updated {{
            color: #666;
            margin-bottom: 30px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th,
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }}

        th {{
            background: #f2f2f2;
        }}

        tr:hover {{
            background: #f7f7f7;
        }}
    </style>
</head>

<body>

<h1>Lurkers.io - {html.escape(gamemode)} Leaderboard</h1>

<div class="updated">
    Last updated: {html.escape(str(updated_at))}
</div>

<table>
    <thead>
        <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>Score</th>
            <th>Kills</th>
            <th>Deaths</th>
            <th>K/D Ratio</th>
            <th>Games Won</th>
            <th>Games Lost</th>
            <th>Win Rate</th>
        </tr>
    </thead>

    <tbody>
        {''.join(rows)}
    </tbody>
</table>

</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(page)

    print(f"Generated {filepath}")


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


# 2. Get Lurkers leaderboards
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

    # Write JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Generate static HTML
    generate_static_html(
        gamemode,
        output["players"],
        output["updatedAt"]
    )

    print(
        f"Updated {len(output['players'])} players "
        f"for {gamemode}."
    )
