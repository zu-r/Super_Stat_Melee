import sys
import time
import requests
import json
import sqlite3
from datetime import datetime
from functools import lru_cache
from src.config import HEADERS, DB_NAME
import datetime

PLAYER_URL = "https://api.liquipedia.net/api/v3/player"

def fetch_players(offset):
    params = {
        "wiki": 'smash',
        "conditions": "[[earnings::>500]] AND [[extradata_maingame::melee]]",
        "query": "pageid,pagename,id,alternateid,name,type,region,nationality,status,extradata,earningsbyyear,earnings,birthdate,teampagename",
        "limit": 1000,
        "groupby": 'earnings DESC',
        "offset": offset
    }
    response = requests.get(PLAYER_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        json_data = response.json()
        now = datetime.datetime.now().strftime('%H:%M:%S')
        filename = f"player_data_time_{now}.json"
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=2)
        print(f"Saved API response to {filename}")
        
        return json_data.get('result', [])
    else:
        print(f"Error fetching players: {response.status_code}")
        return None

def insert_player(player):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    extradata = player['extradata']
    maingame = extradata.get('maingame', '')
    mainmelee = extradata.get('mainmelee', '')
    
    cursor.execute('''
    INSERT OR REPLACE INTO players (
        id, pageid, pagename, alternateid, name, type, nationality, region,
        birthdate, teampagename, status, earnings, earningsbyyear, extradata,
        maingame, mainmelee
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        player['id'],
        player['pageid'],
        player['pagename'],
        player.get('alternateid'),
        player['name'],
        player['type'],
        player['nationality'],
        player['region'],
        player.get('birthdate'),
        player.get('teampagename'),
        player['status'],
        player['earnings'],
        json.dumps(player['earningsbyyear']),
        json.dumps(extradata),
        maingame,
        mainmelee
    ))
    
    conn.commit()
    conn.close()

def update_database(offset):
    players = fetch_players(offset)
    if not players:
        print("No players fetched. Check your offset or API limits.")
        return
    
    for player in players:
        insert_player(player)
    
    print(f"Processed {len(players)} players starting from offset {offset}")
    print("Database updated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <offset>")
        sys.exit(1)
    
    try:
        offset = int(sys.argv[1])
    except ValueError:
        print("Error: Offset must be an integer.")
        sys.exit(1)
    
    update_database(offset)