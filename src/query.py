import sqlite3
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('english'))

def extract_features(question):
    words = word_tokenize(question.lower())
    return {word: True for word in words if word not in stop_words}

def load_classifier(filename='training_data.txt'):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            question, category = line.strip().split('\t')
            data.append((question, category))
    
    featuresets = [(extract_features(q), t) for (q, t) in data]
    return NaiveBayesClassifier.train(featuresets)


classifier = load_classifier()

def natural_language_to_sql(query):
    print(f"Original query: {query}")  
    match = re.search(r'"([^"]*)"', query)
    entity = match.group(1) if match else None
    print(f"Extracted entity: {entity}")  
    
    features = extract_features(query)
    category = classifier.classify(features)
    print(f"Classified category: {category}")  
    
    if category == "tournament_winner":
        sql_query = f"""
        SELECT p.id, t.name as tournament_name
        FROM tournaments t
        JOIN players p ON t.winner_id = p.id
        WHERE t.name LIKE '%{entity}%'
        ORDER BY length('{entity}') - length(t.name)
        LIMIT 1
        """
    elif category == "tournament_runner_up":
        sql_query = f"""
        SELECT p.id, t.name as tournament_name
        FROM tournaments t
        JOIN players p ON t.runnerup_id = p.id
        WHERE t.name LIKE '%{entity}%'
        ORDER BY length('{entity}') - length(t.name)
        LIMIT 1
        """
    elif category == "most_majors_winner":
        sql_query = """
        SELECT p.id, COUNT(*) as major_wins
        FROM tournaments t
        JOIN players p ON t.winner_id = p.id
        WHERE t.liquipediatier = '1'
        GROUP BY p.id
        ORDER BY major_wins DESC
        LIMIT 1
        """
    elif category == "most_tournaments_winner":
        sql_query = """
        SELECT p.id, COUNT(*) as tournament_wins
        FROM tournaments t
        JOIN players p ON t.winner_id = p.id
        GROUP BY p.id
        ORDER BY tournament_wins DESC
        LIMIT 1
        """
    elif category == "player_major_count":
        sql_query = f"""
        SELECT p.id, COUNT(*) as major_wins
        FROM tournaments t
        JOIN players p ON t.winner_id = p.id
        WHERE p.name LIKE '%{entity}%' AND t.liquipediatier = '1'
        GROUP BY p.id
        ORDER BY length(p.name) - length('{entity}')
        LIMIT 1
        """
    elif category == "highest_career_earnings":
        sql_query = """
        SELECT id, earnings
        FROM players
        ORDER BY earnings DESC
        LIMIT 1
        """
    elif category == "earnings_above_threshold":
        sql_query = f"""
        SELECT id, earnings
        FROM players
        WHERE earnings > {entity}
        ORDER BY earnings DESC
        """
    elif category == "country_most_wins":
        sql_query = """
        SELECT winner_country, COUNT(*) as wins
        FROM tournaments
        GROUP BY winner_country
        ORDER BY wins DESC
        LIMIT 1
        """
    elif category == "winners_born_in_year":
        sql_query = f"""
        SELECT COUNT(DISTINCT p.id) as winners
        FROM players p
        JOIN tournaments t ON p.id = t.winner_id
        WHERE strftime('%Y', p.birthdate) = '{entity}'
        """
    elif category == "character_main_major_wins":
        sql_query = f"""
        SELECT p.id, t.name as tournament_name
        FROM tournaments t
        JOIN players p ON t.winner_id = p.id
        WHERE p.mainmelee LIKE '%{entity}%' AND t.liquipediatier = '1'
        """
    elif category == "player_main_character":
        sql_query = f"""
        SELECT id, mainmelee
        FROM players
        WHERE name LIKE '%{entity}%'
        ORDER BY length(name) - length('{entity}')
        LIMIT 1
        """
    elif category == "tournaments_in_city":
        sql_query = f"""
        SELECT name
        FROM tournaments
        WHERE city LIKE '%{entity}%'
        ORDER BY length(city) - length('{entity}')
        """
    elif category == "tournaments_in_country":
        sql_query = f"""
        SELECT name
        FROM tournaments
        WHERE country LIKE '%{entity}%'
        ORDER BY length(country) - length('{entity}')
        """
    else:
        print(f"No SQL query generated for category: {category}")  
        return None

    print(f"Generated SQL query: {sql_query}")  
    return sql_query

def query_database(sql_query):
    conn = sqlite3.connect('super_stat_melee.db')  
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    print(f"Query results: {results}") 
    return results