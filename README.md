# Lurkers.io Leaderboard

A live leaderboard for **Lurkers.io**, providing rankings and statistics across multiple game modes.

The project is independently developed and maintained by **AethericNebula**.

### Website Right Here:
https://aethernebula2-prog.github.io/lurkers.io-leaderboard/

## Features

### 🏆 Live Leaderboards

The leaderboard currently supports:

* **Bedwars**
* **Capture the Flag**
* **Team Deathmatch**

Each leaderboard displays up to the **top 20 players** and includes:

* Rank
* Player
* Score
* Kills
* Deaths
* K/D Ratio
* Total Games
* Games Won
* Games Lost
* Win Rate

Leaderboard data is automatically updated on a regular schedule.

### 📊 Daily History

The project also maintains a daily snapshot of leaderboard data.

Each day's leaderboard is stored separately:

```text
history/
├── 2026-09-09.json
├── 2026-09-10.json
└── ...
```

Each snapshot contains the leaderboard data for all supported game modes:

```json
{
    "bedwars": [],
    "ctf": [],
    "team-deathmatch": []
}
```

This allows historical leaderboard data to be preserved independently from the current live leaderboard.

The history system is handled by a separate GitHub Actions workflow, so a failure in the history system does not interfere with the regular leaderboard data update process.

### 🎨 Themes

The leaderboard includes multiple visual themes:

* Default （Lurkers.io style dark-blue)
* Light
* Dark

The selected theme is saved locally, so it can be preserved between visits.

### 🌐 Multiple Languages

The interface supports multiple languages:

* English
* Chinese
* Japanese
* Spanish
* German
* French
* Italian
* Russian

Language settings are available through the Settings menu.

### 👤 Player Roles

Players can have roles displayed alongside their names.

Supported roles may include:

* DEV
* MOD
* SUP
* VIP
* POO (xD)

Roles are managed separately from the leaderboard data and are identified using the player's `playerId`.

Role assignments are primarily based on the player's actual in-game role in Lurkers.io.

Requests or begging for roles will not be accepted.

### 🔼 Changes

You can see the changes of Rank directly on the leaderboard. In settings you can check Show All Changes to see all changes.

### 🔤 Better Font?

The roles uses **Lurkers** font for the role displays.

This helps give the leaderboard a visual style consistent with Lurkers.io.

### ⚙️ About & Settings

The website includes:

* About panel
* Settings panel
* Language selection
* Theme selection
* Project information
* Other Settings

## Data

Leaderboard data is stored in JSON files and updated automatically.

The current leaderboard files are:

```text
leaderboard-bedwars.json
leaderboard-ctf.json
leaderboard-team-deathmatch.json
```

Historical snapshots are stored separately under:

```text
history/
```

The leaderboard and history systems are intentionally separated so that the live data update process remains independent from historical data collection.

## Technology

The project is built using standard web technologies:

* HTML
* CSS
* JavaScript
* JSON
* GitHub Pages
* GitHub Actions

No backend server is required for the website itself.

## Project Structure

```text
Lurkers.io-Leaderboard/
├── data
    ├── leaderboard-bedwars.html
    ├── leaderboard-ctf.html
    ├── leaderboard-team-deathmatch.html
├── index.html
├── lurkers.ttf
├── leaderboard-bedwars.json
├── leaderboard-ctf.json
├── leaderboard-team-deathmatch.json
├── roles.json
├── ArchivoBlack-Regular.ttf
└── history/
    ├── 2026-09-09.json
    ├── 2026-09-010.json
    └── ...
```

## Updates

The leaderboard data is automatically refreshed on a regular schedule.

A separate daily workflow creates a historical snapshot of the current leaderboards.

This means the project maintains both:

**Current data**

```text
leaderboard-*.json
```

and

**Historical data**

```text
history/YYYY-MM-DD.json
```

## Disclaimer

This project is an independent community project and is not officially affiliated with or endorsed by the developers of Lurkers.io.

Leaderboard data and player statistics are provided for informational purposes.

---
**All Rights Reserved**
**Thanks Bergice Productions**
**Lurkers.io Leaderboard**
Made by **AethericNebula**
Data from **lurkers.io** via **Microsoft PlayFab**
