import sys
import time
import requests
import json
import sqlite3
from datetime import datetime
from functools import lru_cache
from src.config import HEADERS, DB_NAME
import datetime

TOURNAMENT_URL = "https://api.liquipedia.net/api/v3/tournament"

def fetch_tournaments(offset):
    params = {
        "wiki": 'smash',
        "conditions": "[[game::melee]] AND [[liquipediatier::3]]",
        "query": "name,pageid,pagename,shortname,seriespage,game,startdate,enddate,sortdate,locations,prizepool,participantsnumber,liquipediatier,extradata",
        "limit": 1000,
        "groupby": 'startdate DESC',
        "offset": offset
    }
    response = requests.get(TOURNAMENT_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        json_data = response.json()
        now = datetime.datetime.now().strftime('%H:%M:%S')
        filename = f"tournament_data_time_{now}.json"
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=2)
        print(f"Saved API response to {filename}")
        
        return json_data.get('result', [])
    else:
        print(f"Error fetching tournaments: {response.status_code}")
        return None

def insert_tournament(tournament):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR REPLACE INTO tournaments (
        pageid, pagename, name, shortname, seriespage, game, startdate, enddate,
        sortdate, locations, city, country, prizepool, participantsnumber,
        liquipediatier, extradata, winner_id, runnerup_id, winner_characters,
        runnerup_characters, winner_country, runnerup_country
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        tournament['pageid'],
        tournament['pagename'],
        tournament['name'],
        tournament['shortname'],
        tournament.get('seriespage'),
        tournament['game'],
        tournament['startdate'],
        tournament['enddate'],
        tournament['sortdate'],
        json.dumps(tournament['locations']),
        tournament['locations'].get('city1'),
        tournament['locations'].get('country1'),
        tournament['prizepool'],
        tournament['participantsnumber'],
        tournament['liquipediatier'],
        json.dumps(tournament['extradata']),
        tournament['extradata'].get('winnerlink'),
        tournament['extradata'].get('runneruplink'),
        tournament['extradata'].get('winnerheads'),
        tournament['extradata'].get('runnerupheads'),
        tournament['extradata'].get('winnerflag'),
        tournament['extradata'].get('runnerupflag')
    ))
    
    conn.commit()
    conn.close()

def update_database(offset):
    tournaments = fetch_tournaments(offset)
    if not tournaments:
        print("No tournaments fetched. Check your offset or API limits.")
        return
    
    for tournament in tournaments:
        insert_tournament(tournament)
    
    print(f"Processed {len(tournaments)} tournaments starting from offset {offset}")
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