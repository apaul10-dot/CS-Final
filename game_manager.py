from standings import Standings, Competition
from typing import Dict, List, Optional
from dataclasses import dataclass
import random
from enum import Enum
import pandas as pd

class Competition(Enum):
    LA_LIGA = "La Liga"
    CHAMPIONS_LEAGUE = "Champions League"
    COPA_DEL_REY = "Copa del Rey"
    SUPERCUPA = "Supercopa de España"

@dataclass
class Player:
    name: str
    position: str
    rating: int
    stats: Dict[str, int]

@dataclass
class TeamStats:
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0
    goal_diff: int = 0

class GameManager:
    def __init__(self):
        self.standings: Dict[Competition, Dict[str, TeamStats]] = {}
        self.players = self._initialize_players()
        self.current_team = "FC Barcelona"
        self.money = 100_000_000  # Starting budget in euros
        self.season = "2024-25"
        self._initialize_teams()
        
    def _initialize_teams(self):
        # La Liga teams (20 teams)
        self.standings[Competition.LA_LIGA] = {
            team: TeamStats() for team in [
                "FC Barcelona", "Real Madrid", "Atletico Madrid", "Real Sociedad",
                "Real Betis", "Athletic Bilbao", "Valencia", "Villarreal",
                "Celta Vigo", "Osasuna", "Getafe", "Girona",
                "Deportivo Alaves", "Leganes", "Mallorca", "Las Palmas",
                "Rayo Vallecano", "Espanyol", "Sevilla", "Real Valladolid"
            ]
        }
        
        # Champions League teams (36 teams in new format)
        self.standings[Competition.CHAMPIONS_LEAGUE] = {
            team: TeamStats() for team in [
                # Pot 1 (Top teams)
                "Manchester City", "Bayern Munich", "Real Madrid", "PSG",
                "Liverpool", "Inter Milan", "Borussia Dortmund", "Barcelona",
                # Pot 2
                "Atletico Madrid", "RB Leipzig", "Porto", "Arsenal",
                "Napoli", "Benfica", "Bayer Leverkusen", "Atalanta",
                # Pot 3
                "Red Bull Salzburg", "Shakhtar Donetsk", "Red Star Belgrade",
                "Young Boys", "Royal Antwerp", "Celtic", "Feyenoord",
                "AC Milan", "Lazio", "PSV Eindhoven", "Sporting CP",
                # Pot 4
                "Real Sociedad", "Crvena Zvezda", "Newcastle United",
                "Union Berlin", "Lens", "Braga", "Royal Union",
                "Sturm Graz", "Sparta Prague", "Slovan Bratislava"
            ]
        }
        
        # Copa del Rey teams (Round of 32)
        self.standings[Competition.COPA_DEL_REY] = {
            team: TeamStats() for team in [
                "FC Barcelona", "Real Madrid", "Atletico Madrid", "Real Sociedad",
                "Real Betis", "Athletic Bilbao", "Valencia", "Villarreal",
                "Celta Vigo", "Osasuna", "Getafe", "Girona",
                "Deportivo Alaves", "Leganes", "Mallorca", "Las Palmas",
                "Rayo Vallecano", "Espanyol", "Sevilla", "Real Valladolid",
                "Unionistas", "Amorebieta", "Tenerife", "Racing Santander",
                "Eldense", "Burgos", "Mirandes", "Alcorcon",
                "Cartagena", "Huesca", "Zaragoza", "Levante"
            ]
        }
        
        # Supercopa teams (4 teams)
        self.standings[Competition.SUPERCUPA] = {
            team: TeamStats() for team in [
                "FC Barcelona",  # La Liga champions
                "Real Madrid",   # La Liga runners-up
                "Athletic Bilbao",  # Copa del Rey winners
                "Mallorca"       # Copa del Rey runners-up
            ]
        }
    
    def _initialize_players(self) -> Dict[str, List[Player]]:
        """Initialize all players with their stats"""
        players = {
            "Goalkeepers": [],
            "Centerbacks": [],
            "Rightbacks": [],
            "Leftbacks": [],
            "Midfielders": [],
            "Wingers": [],
            "Strikers": []
        }
        
        # Goalkeepers
        goalkeeper_stats = {
            "Marc-Andre ter Stegan": {"diving": 92, "handling": 65, "kicking": 90, "reflexes": 90, "speed": 82, "positioning": 88},
            "Inaki Pena": {"diving": 78, "handling": 75, "kicking": 72, "reflexes": 80, "speed": 70, "positioning": 76},
            "Wojciech Szczesny": {"diving": 86, "handling": 84, "kicking": 80, "reflexes": 88, "speed": 72, "positioning": 85},
            "Ander Astralaga": {"diving": 65, "handling": 62, "kicking": 60, "reflexes": 68, "speed": 65, "positioning": 63},
            "Deigo Kochen": {"diving": 65, "handling": 63, "kicking": 61, "reflexes": 67, "speed": 66, "positioning": 64},
            "Aron Yaakobishvili": {"diving": 55, "handling": 52, "kicking": 50, "reflexes": 58, "speed": 54, "positioning": 53}
        }
        
        keeper_ratings = {
            "Marc-Andre ter Stegan": 85, "Inaki Pena": 72, "Wojciech Szczesny": 89,
            "Ander Astralaga": 60, "Deigo Kochen": 60, "Aron Yaakobishvili": 50
        }
        
        for name, stats in goalkeeper_stats.items():
            players["Goalkeepers"].append(Player(name, "Goalkeeper", keeper_ratings[name], stats))
        
        # Centerbacks
        centerback_stats = {
            "Pau Cubarsi": {"pace": 90, "shooting": 75, "passing": 95, "dribbling": 92, "defending": 88, "physicality": 88},
            "Ronald Araujo": {"pace": 97, "shooting": 77, "passing": 88, "dribbling": 80, "defending": 92, "physicality": 92},
            "Inigo Martinez": {"pace": 85, "shooting": 80, "passing": 97, "dribbling": 85, "defending": 97, "physicality": 92},
            "Andreas Christensen": {"pace": 85, "shooting": 74, "passing": 85, "dribbling": 50, "defending": 70, "physicality": 80},
            "Sergi Dominguez": {"pace": 85, "shooting": 60, "passing": 70, "dribbling": 50, "defending": 70, "physicality": 80},
            "Eric Garcia": {"pace": 85, "shooting": 60, "passing": 70, "dribbling": 50, "defending": 70, "physicality": 80}
        }
        
        centerback_ratings = {
            "Pau Cubarsi": 95, "Ronald Araujo": 90, "Inigo Martinez": 97,
            "Andreas Christensen": 85, "Sergi Dominguez": 73, "Eric Garcia": 87
        }
        
        for name, stats in centerback_stats.items():
            players["Centerbacks"].append(Player(name, "Centerback", centerback_ratings[name], stats))
        
        # Add other positions with their stats and ratings
        # Rightbacks
        rightback_ratings = {"Jules Kounde": 95, "Hector Fort": 80}
        for name, rating in rightback_ratings.items():
            players["Rightbacks"].append(Player(name, "Rightback", rating, {}))
        
        # Leftbacks
        leftback_ratings = {"Alejandro Balde": 95, "Gerad Martin": 88}
        for name, rating in leftback_ratings.items():
            players["Leftbacks"].append(Player(name, "Leftback", rating, {}))
        
        # Midfielders
        midfielder_ratings = {
            "Gavi": 88, "Pedri": 99, "Pablo Torre": 80, "Fermin Lopez": 85,
            "Marc Casado": 92, "Dani Olmo": 92, "Frenkie De Jong": 95, "Marc Barnal": 80
        }
        for name, rating in midfielder_ratings.items():
            players["Midfielders"].append(Player(name, "Midfielder", rating, {}))
        
        # Wingers
        winger_ratings = {
            "Ansu Fati": 80, "Raphinha": 99, "Lamine Yamal": 99, "Pau Victor": 82
        }
        for name, rating in winger_ratings.items():
            players["Wingers"].append(Player(name, "Winger", rating, {}))
        
        # Strikers
        striker_ratings = {"Robert Lewandowski": 95, "Ferran Torres": 90}
        for name, rating in striker_ratings.items():
            players["Strikers"].append(Player(name, "Striker", rating, {}))
        
        return players
    
    def get_team_squad(self) -> Dict[str, List[Player]]:
        """Get the current team's squad"""
        return self.players
    
    def update_match_result(self, competition: Competition, home_team: str, away_team: str, 
                          home_goals: int, away_goals: int):
        """Update standings based on match result"""
        if competition not in self.standings:
            raise ValueError(f"Invalid competition: {competition}")
        
        if home_team not in self.standings[competition] or away_team not in self.standings[competition]:
            raise ValueError(f"Invalid team(s) for {competition}")
        
        # Update home team stats
        home_stats = self.standings[competition][home_team]
        home_stats.played += 1
        home_stats.goals_for += home_goals
        home_stats.goals_against += away_goals
        home_stats.goal_diff = home_stats.goals_for - home_stats.goals_against
        
        # Update away team stats
        away_stats = self.standings[competition][away_team]
        away_stats.played += 1
        away_stats.goals_for += away_goals
        away_stats.goals_against += home_goals
        away_stats.goal_diff = away_stats.goals_for - away_stats.goals_against
        
        # Update points and results
        if home_goals > away_goals:
            home_stats.wins += 1
            home_stats.points += 3
            away_stats.losses += 1
        elif home_goals < away_goals:
            away_stats.wins += 1
            away_stats.points += 3
            home_stats.losses += 1
        else:
            home_stats.draws += 1
            away_stats.draws += 1
            home_stats.points += 1
            away_stats.points += 1
    
    def get_standings(self, competition: Competition) -> List[tuple]:
        """Get sorted standings for a competition"""
        if competition not in self.standings:
            raise ValueError(f"Invalid competition: {competition}")
        
        # Sort teams by points, then goal difference, then goals scored
        standings = []
        for team, stats in self.standings[competition].items():
            standings.append((
                team,
                stats.played,
                stats.wins,
                stats.draws,
                stats.losses,
                stats.goals_for,
                stats.goals_against,
                stats.goal_diff,
                stats.points
            ))
        
        return sorted(standings, key=lambda x: (-x[8], -x[7], -x[5]))
    
    def print_team_squad(self):
        """Print the current team's squad"""
        print(f"\n=== {self.current_team} Squad {self.season} ===\n")
        
        for position, players in self.players.items():
            print(f"\n{position}:")
            print("-" * 50)
            print(f"{'Name':<25} {'Rating':<8} {'Position':<15}")
            print("-" * 50)
            
            for player in sorted(players, key=lambda x: x.rating, reverse=True):
                print(f"{player.name:<25} {player.rating:<8} {player.position:<15}")
    
    def get_standings_data(self, competition: Competition) -> pd.DataFrame:
        """Get standings data as a DataFrame for Streamlit display"""
        standings = self.get_standings(competition)
        
        # Create DataFrame
        df = pd.DataFrame(standings, columns=[
            'Team', 'Played', 'Won', 'Drawn', 'Lost', 
            'Goals For', 'Goals Against', 'Goal Difference', 'Points'
        ])
        
        # Add position column
        df.insert(0, 'Pos', range(1, len(df) + 1))
        
        return df

    def print_standings(self, competition: Competition):
        """Print formatted standings table"""
        standings = self.get_standings(competition)
        
        # Print header
        print(f"{'Pos':<4} {'Team':<20} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<3} {'GA':<3} {'GD':<3} {'Pts':<3}")
        print("-" * 60)
        
        # Print team rows
        for pos, (team, played, wins, draws, losses, gf, ga, gd, pts) in enumerate(standings, 1):
            print(f"{pos:<4} {team:<20} {played:<3} {wins:<3} {draws:<3} {losses:<3} {gf:<3} {ga:<3} {gd:<3} {pts:<3}")
    
    def print_all_standings(self):
        """Print standings for all competitions"""
        print(f"\n=== {self.season} Season Standings ===\n")
        
        for competition in Competition:
            self.print_standings(competition)

    def simulate_match(self, competition: Competition, home_team: str, away_team: str) -> tuple:
        """Simulate a match and return the score"""
        # Generate realistic scores based on competition
        if competition == Competition.LA_LIGA:
            # La Liga typically has lower scoring matches
            home_goals = random.randint(0, 3)
            away_goals = random.randint(0, 2)
        elif competition == Competition.CHAMPIONS_LEAGUE:
            # Champions League can have higher scoring matches
            home_goals = random.randint(0, 4)
            away_goals = random.randint(0, 3)
        elif competition == Competition.COPA_DEL_REY:
            # Copa del Rey can have varied scores
            home_goals = random.randint(0, 4)
            away_goals = random.randint(0, 4)
        else:  # Supercopa
            # Supercopa typically has close matches
            home_goals = random.randint(0, 2)
            away_goals = random.randint(0, 2)
        
        # Update standings with the result
        self.update_match_result(competition, home_team, away_team, home_goals, away_goals)
        
        return home_goals, away_goals

def main():
    # Create game manager instance
    game = GameManager()
    
    # Print initial squad
    game.print_team_squad()
    
    # Simulate some matches
    print("\n=== Simulating Matches ===\n")
    
    # La Liga matches
    home_goals, away_goals = game.simulate_match(Competition.LA_LIGA, "FC Barcelona", "Real Madrid")
    print(f"La Liga: FC Barcelona {home_goals}-{away_goals} Real Madrid")
    
    # Champions League matches
    home_goals, away_goals = game.simulate_match(Competition.CHAMPIONS_LEAGUE, "Barcelona", "Bayern Munich")
    print(f"Champions League: Barcelona {home_goals}-{away_goals} Bayern Munich")
    
    # Print updated standings
    game.print_all_standings()

if __name__ == "__main__":
    main() 