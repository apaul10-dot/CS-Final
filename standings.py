from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class Competition(Enum):
    LA_LIGA = "La Liga"
    CHAMPIONS_LEAGUE = "Champions League"
    COPA_DEL_REY = "Copa del Rey"
    SUPERCOPA = "Supercopa de España"

@dataclass
class TeamStats:
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    
    @property
    def points(self) -> int:
        return (self.won * 3) + self.drawn
    
    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

class Standings:
    def __init__(self):
        self.standings: Dict[Competition, Dict[str, TeamStats]] = {
            Competition.LA_LIGA: {},
            Competition.CHAMPIONS_LEAGUE: {},
            Competition.COPA_DEL_REY: {},
            Competition.SUPERCOPA: {}
        }
        self._initialize_teams()
    
    def _initialize_teams(self):
        # Initialize La Liga teams (2024-25 season)
        la_liga_teams = [
            "FC Barcelona", "Real Madrid", "Atletico Madrid", "Real Sociedad", 
            "Real Betis", "Athletic Bilbao", "Valencia", "Villarreal", 
            "Celta Vigo", "Osasuna", "Getafe", "Girona", "Deportivo Alaves", 
            "Leganes", "Mallorca", "Las Palmas", "Rayo Vallecano", 
            "Espanyol", "Sevilla", "Real Vallladolid"
        ]
        
        # Initialize Champions League teams (2024-25 new format)
        # Top 8 teams from 2023-24 season
        champions_league_teams = [
            # Pot 1 (League Champions)
            "Manchester City", "Barcelona", "Bayern Munich", "Napoli", 
            "PSG", "Feyenoord", "Benfica", "Celtic",
            
            # Pot 2 (Strong teams)
            "Real Madrid", "Manchester United", "Inter Milan", "Borussia Dortmund",
            "Atletico Madrid", "RB Leipzig", "Porto", "Arsenal",
            
            # Pot 3 (Other qualified teams)
            "AC Milan", "Lazio", "Red Bull Salzburg", "Red Star Belgrade",
            "PSV Eindhoven", "Braga", "Royal Antwerp", "Crvena Zvezda",
            
            # Pot 4 (Remaining teams)
            "Young Boys", "Royal Union", "Sturm Graz", "Slovan Bratislava",
            "Dinamo Zagreb", "Sparta Prague", "Bologna", "Stuttgart"
        ]
        
        # Initialize Copa del Rey teams (2024-25 season)
        copa_del_rey_teams = [
            # Round of 32 teams
            "Barcelona", "Real Madrid", "Atletico Madrid", "Real Sociedad",
            "Athletic Bilbao", "Valencia", "Villarreal", "Real Betis",
            "Girona", "Osasuna", "Getafe", "Mallorca",
            "Celta Vigo", "Alaves", "Las Palmas", "Rayo Vallecano",
            "Espanyol", "Sevilla", "Valladolid", "Leganes",
            "Burgos", "Eibar", "Mirandes", "Racing Santander",
            "Elche", "Levante", "Huesca", "Tenerife",
            "Cartagena", "Alcorcon", "Amorebieta", "Unionistas"
        ]
        
        # Initialize Supercopa teams (2024-25 season)
        supercopa_teams = [
            "Real Madrid",  # La Liga 2023-24 champions
            "Athletic Bilbao",  # Copa del Rey 2023-24 winners
            "Barcelona",  # La Liga 2023-24 runners-up
            "Mallorca"  # Copa del Rey 2023-24 runners-up
        ]
        
        # Initialize standings for each competition
        for team in la_liga_teams:
            self.standings[Competition.LA_LIGA][team] = TeamStats()
            
        for team in champions_league_teams:
            self.standings[Competition.CHAMPIONS_LEAGUE][team] = TeamStats()
            
        for team in copa_del_rey_teams:
            self.standings[Competition.COPA_DEL_REY][team] = TeamStats()
            
        for team in supercopa_teams:
            self.standings[Competition.SUPERCOPA][team] = TeamStats()
    
    def update_match_result(self, competition: Competition, home_team: str, away_team: str, 
                          home_goals: int, away_goals: int):
        """Update standings based on match result"""
        if competition not in self.standings:
            raise ValueError(f"Invalid competition: {competition}")
            
        if home_team not in self.standings[competition] or away_team not in self.standings[competition]:
            raise ValueError("One or both teams not found in competition")
            
        # Update home team stats
        home_stats = self.standings[competition][home_team]
        home_stats.played += 1
        home_stats.goals_for += home_goals
        home_stats.goals_against += away_goals
        
        # Update away team stats
        away_stats = self.standings[competition][away_team]
        away_stats.played += 1
        away_stats.goals_for += away_goals
        away_stats.goals_against += home_goals
        
        # Update wins/draws/losses
        if home_goals > away_goals:
            home_stats.won += 1
            away_stats.lost += 1
        elif home_goals < away_goals:
            away_stats.won += 1
            home_stats.lost += 1
        else:
            home_stats.drawn += 1
            away_stats.drawn += 1
    
    def get_standings(self, competition: Competition) -> List[Tuple[str, TeamStats]]:
        """Get sorted standings for a competition"""
        if competition not in self.standings:
            raise ValueError(f"Invalid competition: {competition}")
            
        standings = list(self.standings[competition].items())
        return sorted(standings, 
                     key=lambda x: (x[1].points, x[1].goal_difference, x[1].goals_for),
                     reverse=True)
    
    def print_standings(self, competition: Competition):
        """Print formatted standings table for a competition"""
        standings = self.get_standings(competition)
        
        print(f"\n{competition.value} Standings")
        print("-" * 80)
        print(f"{'Pos':<4} {'Team':<25} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<3} {'GA':<3} {'GD':<3} {'Pts':<3}")
        print("-" * 80)
        
        for pos, (team, stats) in enumerate(standings, 1):
            print(f"{pos:<4} {team:<25} {stats.played:<3} {stats.won:<3} {stats.drawn:<3} "
                  f"{stats.lost:<3} {stats.goals_for:<3} {stats.goals_against:<3} "
                  f"{stats.goal_difference:<3} {stats.points:<3}")
        print("-" * 80) 