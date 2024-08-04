import os

API_KEY = os.getenv("LIQUIPEDIA_API_KEY")
API_URL = "https://api.liquipedia.net/api/v3"
TOURNAMENT_URL = "https://api.liquipedia.net/api/v3/tournament"
HEADERS = {
    "Authorization": f"Apikey {API_KEY}",
    "Accept-Encoding": "gzip",
    "User-Agent": "SuperStatMelee/1.0 (zuwee01@gmail.com)"
}
DB_NAME = "super_stat_melee.db"