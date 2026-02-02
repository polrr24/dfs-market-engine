import requests
import sqlite3
import time
from datetime import datetime

DB_PATH = "data/dfs.db"
URL = "https://api.prizepicks.com/projections?per_page=500"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://app.prizepicks.com/",
    "Origin": "https://app.prizepicks.com"
}


def get_conn():
    return sqlite3.connect(DB_PATH)


def fetch_projections():
    time.sleep(2)  # be polite

    r = requests.get(URL, headers=HEADERS, timeout=15)

    if r.status_code == 429:
        print("⚠️ PrizePicks rate limited (429). Skipping run.")
        return None

    r.raise_for_status()
    return r.json()


def build_player_lookup(included):
    players = {}
    for item in included:
        if item["type"] == "new_player":
            players[item["id"]] = item["attributes"]["name"]
    return players


def build_league_lookup(included):
    leagues = {}
    for item in included:
        if item["type"] == "league":
            leagues[item["id"]] = item["attributes"]["name"]
    return leagues


def normalize_projection(item, player_lookup, league_lookup):
    try:
        attr = item["attributes"]
        rels = item["relationships"]

        player_id = rels["new_player"]["data"]["id"]
        league_id = rels["league"]["data"]["id"]

        return {
            "app": "PrizePicks",
            "player": player_lookup.get(player_id, "UNKNOWN"),
            "stat": attr["stat_type"],
            "line": float(attr["line_score"]),
            "league": league_lookup.get(league_id, "UNKNOWN"),
        }
    except Exception:
        return None


def run_once():
    payload = fetch_projections()
    if not payload:
        return

    data = payload.get("data", [])
    included = payload.get("included", [])

    player_lookup = build_player_lookup(included)
    league_lookup = build_league_lookup(included)

    rows = []
    for item in data:
        row = normalize_projection(item, player_lookup, league_lookup)
        if row and row["player"] != "UNKNOWN":
            rows.append(row)

    conn = get_conn()
    cur = conn.cursor()

    inserted = 0
    for r in rows:
        cur.execute("""
            INSERT OR IGNORE INTO dfs_props (app, player, stat, line, league)
            VALUES (?, ?, ?, ?, ?)
        """, (
            r["app"],
            r["player"],
            r["stat"],
            r["line"],
            r["league"]
        ))
        inserted += 1

    conn.commit()
    conn.close()

    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] "
        f"Inserted {inserted} PrizePicks props"
    )


if __name__ == "__main__":
    while True:
        run_once()
        time.sleep(90)
    
