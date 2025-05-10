'''
Project Name:  "Barca Manager: Build Your Legacy"
Student Name: Arkajit Paul
Date: Wednesday, 07 May 2025
Course: ICS3U-02
This is a program exploring the world of football management, mainly in the context of FC Barcelona. FC Barcelona is one of the best clubs in the history of soccer and 
has a rich history of success and talent. The club has won a total of 27 La Liga titles, 31 Copa del Rey titles, 13 Supercopa de España titles, and 5 UEFA Champions League titles. Throughout this progarm
it will exlore managing Barcelona and making descions that will impact the club's future.. 
'''
import math

# Dictionaries with player names

Goalkeepers=["Marc-Andre ter Stegan", "Inaki Pena", "Wojciech Szczesny", "Ander Astralaga", "Deigo Kochen", "Aron Yaakobishvili"]
Centerbacks=["Pau Cubarsi", "Ronald Araujo", "Inigo Martinez", "Andreas Christensen", "Sergi Dominguez", "Eric Garcia"]
Rightbacks=["Jules Kounde", "Hector Fort"]
Leftbacks=["Alejandro Balde", "Gerad Martin"]
Midfielders=["Gavi", "Pedri", "Pablo Torre", "Fermin Lopez", "Marc Casado", "Dani Olmo", "Frenkie De Jong", "Marc Barnal"]
Wingers=["Ansu Fati", "Raphinha", "Lamine Yamal", "Pau Victor"]
Strikers=["Robert Lewandowski", "Ferran Torres"]

#Dictionary with player ratings based on how much Flick starts them
keeper_ratings = {"Marc-Andre ter Stegan": 85, "Inaki Pena": 72, "Wojciech Szczesny": 89, "Ander Astralaga": 60, "Deigo Kochen": 60, "Aron Yaakobishvili": 50}
centerback_ratings = {"Pau Cubarsi": 95, "Ronald Araujo": 90, "Inigo Martinez": 97, "Andreas Christensen": 85, "Sergi Dominguez": 73, "Eric Garcia": 87}
rightback_ratings = {"Jules Kounde": 95, "Hector Fort": 80}
leftback_ratings = {"Alejandro Balde": 95, "Gerad Martin": 88}
midfielder_ratings = {"Gavi": 88, "Pedri": 99, "Pablo Torre": 80, "Fermin Lopez": 85, "Marc Casado": 92, "Dani Olmo": 92, "Frenkie De Jong": 95, "Marc Barnal": 80}
winger_ratings = {"Ansu Fati": 80, "Raphinha": 99, "Lamine Yamal": 99, "Pau Victor": 82}
striker_ratings = {"Robert Lewandowski": 95, "Ferran Torres": 90}

#Dictionaries on stats of players
goalkeeper_stats = {
    "Marc-Andre ter Stegan": {
        "diving": 92,
        "handling": 65,
        "kicking": 90,
        "reflexes": 90,
        "speed": 82,
        "positioning": 88
    },
    "Inaki Pena": {
        "diving": 78,
        "handling": 75,
        "kicking": 72,
        "reflexes": 80,
        "speed": 70,
        "positioning": 76
    },
    "Wojciech Szczesny": {
        "diving": 86,
        "handling": 84,
        "kicking": 80,
        "reflexes": 88,
        "speed": 72,
        "positioning": 85
    },
    "Ander Astralaga": {
        "diving": 65,
        "handling": 62,
        "kicking": 60,
        "reflexes": 68,
        "speed": 65,
        "positioning": 63
    },
    "Deigo Kochen": {
        "diving": 65,
        "handling": 63,
        "kicking": 61,
        "reflexes": 67,
        "speed": 66,
        "positioning": 64
    },
    "Aron Yaakobishvili": {
        "diving": 55,
        "handling": 52,
        "kicking": 50,
        "reflexes": 58,
        "speed": 54,
        "positioning": 53
    }
}

centerback_stats = {
    "Pau Cubarsi": {
        "pace": 90,
        "shooting": 75,
        "passing": 95,
        "dribbling": 92,
        "defending": 88,
        "physicality": 88
    },
    "Ronald Araujo": {
        "pace": 97,
        "shooting": 77,
        "passing": 88,
        "dribbling": 80,
        "defending": 92,
        "physicality": 92
    },
    "Inigo Martinez": {
        "pace": 85,
        "shooting": 80,
        "passing": 97,
        "dribbling": 85,
        "defending": 97,
        "physicality": 92
    },
    "Andreas Christensen": {
        "pace": 85,
        "shooting": 74,
        "passing": 85,
        "dribbling": 50,
        "defending": 70,
        "physicality": 80
    },
    "Sergi Dominguez": {
        "pace": 85,
        "shooting": 60,
        "passing": 70,
        "dribbling": 50,
        "defending": 70,
        "physicality": 80
    },
    "Eric Garcia": {
        "pace": 85,
        "shooting": 60,
        "passing": 70,
        "dribbling": 50,
        "defending": 70,
        "physicality": 80
    }
}

competitions=["La Liga", "Champions League", "Copa del Rey", "Supercopa de España"] #List of competition 2024-2025 Season

#List of teams in each competition in 2024-2025 season
la_liga_teams=["FC Barcelona", "Real Madrid", "Atletico Madrid", "Real Sociedad", "Real Betis", "Athletic Bilbao", "Valencia", "Villarreal", "Celta Vigo", "Osasuna", "Getafe", "Girona", "Deportivo Alaves", "Leganes", "Mallorca", "Las Palmas", "Rayo Vallecano", "Espanyol", "Sevilla", "Real Vallladolid"]

champions_league_teams = [
    "Liverpool", "Barcelona", "Arsenal", "Inter Milan", "Atletico Madrid", "Bayer Leverkusen",
    "LOSC Lille", "Atalanta", "Dortmund", "Real Madrid", "Bayern Munich", "AC Milan",
    "PSV Eindhoven", "Manchester City", "Manchester United", "FC Porto", "Benfica",
    "RB Leipzig", "Napoli", "Real Sociedad", "Paris Saint-Germain", "Monaco", "Brest",
    "Feyenoord", "Juventus", "Celtic", "Sporting", "Club Brugge", "Dinamo Zagreb",
    "VfB Stuttgart", "Shakhtar Donetsk", "Bologna", "Crvena Zvezda", "SK Sturm Graz",
    "Sparta Prague", "RB Salzburg", "Slovan Bratislava", "Young Boys"
]

copa_del_rey_matchups=["Ourense vs Valencia", "Almeria vs Leganes", "Pontevedra vs Getafe", "Barcelona vs Real Betis", "Elche vs Atletico Madrid", "Athletic Bilbao vs Osasuna", "Real Sociedad vs Rayo Vallecano", "Real Madrid vs Celta Vigo"]

supercopa_de_espana_matchups = ["Athletic Bilbao vs Barcelona", "Real Madrid vs Mallorca"]
