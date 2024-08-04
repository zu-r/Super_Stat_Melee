import sqlite3
from src.config import DB_NAME

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS players')
    print("Players table dropped successfully.")

    cursor.execute('''
    CREATE TABLE players (
        id TEXT PRIMARY KEY,
        pageid INTEGER,
        pagename TEXT,
        alternateid TEXT,
        name TEXT,
        type TEXT,
        nationality TEXT,
        region TEXT,
        birthdate DATE,
        teampagename TEXT,
        status TEXT,
        earnings REAL,
        earningsbyyear TEXT,
        extradata TEXT,
        maingame TEXT,
        mainmelee TEXT
    )
    ''')
    print("Players table created successfully.")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tournaments (
        pageid INTEGER PRIMARY KEY,
        pagename TEXT,
        name TEXT,
        shortname TEXT,
        seriespage TEXT,
        game TEXT,
        startdate TEXT,
        enddate TEXT,
        sortdate TEXT,
        locations TEXT,
        city TEXT,
        country TEXT,
        prizepool INTEGER,
        participantsnumber INTEGER,
        liquipediatier TEXT,
        extradata TEXT,
        winner_id TEXT,
        runnerup_id TEXT,
        winner_characters TEXT,
        runnerup_characters TEXT,
        winner_country TEXT,
        runnerup_country TEXT,
        FOREIGN KEY (winner_id) REFERENCES players(id),
        FOREIGN KEY (runnerup_id) REFERENCES players(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Database and tables setup completed successfully.")

if __name__ == "__main__":
    create_database()