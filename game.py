import streamlit as st
import random
import pandas as pd
import time
import numpy as np
from game_manager import GameManager, Competition

# Set page config
st.set_page_config(
    page_title="FC Barcelona Manager",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better formatting
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom, #1D2B53, #A31F34);
    }
    .stButton>button {
        background-color: #1D2B53;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: 2px solid #FFD700;
        font-weight: bold;
        font-size: 1.2em;
    }
    .stButton>button:hover {
        background-color: #A31F34;
        border-color: #FFD700;
    }
    .player-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        border: 2px solid #1D2B53;
    }
    .selected-player {
        background-color: #FFD700;
        border: 2px solid #A31F34;
    }
    h1, h2, h3 {
        color: #FFD700;
        text-align: center;
        font-weight: bold;
    }
    .stProgress > div > div > div {
        background-color: #FFD700;
    }
    .match-result {
        text-align: center;
        font-size: 2em;
        font-weight: bold;
        color: #FFD700;
        padding: 20px;
        border: 3px solid #FFD700;
        border-radius: 15px;
        margin: 20px 0;
    }
    .player-stats {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .standings-table {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Player roster (from stats.py)
player_roster = {
    # Goalkeepers
    'Marc-Andre ter Stegan': {'position': 'GK', 'rating': 85, 'stamina': 100, 'form': 100},
    'Inaki Pena': {'position': 'GK', 'rating': 72, 'stamina': 100, 'form': 100},
    'Wojciech Szczesny': {'position': 'GK', 'rating': 89, 'stamina': 100, 'form': 100},
    # Centerbacks
    'Pau Cubarsi': {'position': 'DEF', 'rating': 95, 'stamina': 100, 'form': 100},
    'Ronald Araujo': {'position': 'DEF', 'rating': 90, 'stamina': 100, 'form': 100},
    'Inigo Martinez': {'position': 'DEF', 'rating': 97, 'stamina': 100, 'form': 100},
    'Andreas Christensen': {'position': 'DEF', 'rating': 85, 'stamina': 100, 'form': 100},
    'Sergi Dominguez': {'position': 'DEF', 'rating': 73, 'stamina': 100, 'form': 100},
    'Eric Garcia': {'position': 'DEF', 'rating': 87, 'stamina': 100, 'form': 100},
    # Fullbacks
    'Jules Kounde': {'position': 'DEF', 'rating': 95, 'stamina': 100, 'form': 100},
    'Hector Fort': {'position': 'DEF', 'rating': 80, 'stamina': 100, 'form': 100},
    'Alejandro Balde': {'position': 'DEF', 'rating': 95, 'stamina': 100, 'form': 100},
    'Gerad Martin': {'position': 'DEF', 'rating': 88, 'stamina': 100, 'form': 100},
    # Midfielders
    'Gavi': {'position': 'MID', 'rating': 88, 'stamina': 100, 'form': 100},
    'Pedri': {'position': 'MID', 'rating': 99, 'stamina': 100, 'form': 100},
    'Pablo Torre': {'position': 'MID', 'rating': 80, 'stamina': 100, 'form': 100},
    'Fermin Lopez': {'position': 'MID', 'rating': 85, 'stamina': 100, 'form': 100},
    'Marc Casado': {'position': 'MID', 'rating': 92, 'stamina': 100, 'form': 100},
    'Dani Olmo': {'position': 'MID', 'rating': 92, 'stamina': 100, 'form': 100},
    'Frenkie De Jong': {'position': 'MID', 'rating': 95, 'stamina': 100, 'form': 100},
    'Marc Barnal': {'position': 'MID', 'rating': 80, 'stamina': 100, 'form': 100},
    # Wingers
    'Ansu Fati': {'position': 'FWD', 'rating': 80, 'stamina': 100, 'form': 100},
    'Raphinha': {'position': 'FWD', 'rating': 99, 'stamina': 100, 'form': 100},
    'Lamine Yamal': {'position': 'FWD', 'rating': 99, 'stamina': 100, 'form': 100},
    'Pau Victor': {'position': 'FWD', 'rating': 82, 'stamina': 100, 'form': 100},
    # Strikers
    'Robert Lewandowski': {'position': 'FWD', 'rating': 95, 'stamina': 100, 'form': 100},
    'Ferran Torres': {'position': 'FWD', 'rating': 90, 'stamina': 100, 'form': 100}
}

# Add tactical formations
FORMATIONS = {
    "4-3-3": {
        "GK": 1,
        "DEF": 4,
        "MID": 3,
        "FWD": 3
    },
    "4-4-2": {
        "GK": 1,
        "DEF": 4,
        "MID": 4,
        "FWD": 2
    },
    "3-5-2": {
        "GK": 1,
        "DEF": 3,
        "MID": 5,
        "FWD": 2
    }
}

# Add match events
MATCH_EVENTS = {
    "GOAL": {
        "probability": 0.1,
        "description": "GOAL!",
        "impact": 1
    },
    "SAVE": {
        "probability": 0.15,
        "description": "Great save!",
        "impact": 0
    },
    "MISS": {
        "probability": 0.2,
        "description": "Missed opportunity!",
        "impact": 0
    },
    "FOUL": {
        "probability": 0.1,
        "description": "Foul committed!",
        "impact": -0.1
    },
    "CARD": {
        "probability": 0.05,
        "description": "Yellow card!",
        "impact": -0.2
    },
    "INJURY": {
        "probability": 0.02,
        "description": "Player injured!",
        "impact": -0.5
    }
}

# Initialize game manager
if 'game_manager' not in st.session_state:
    st.session_state.game_manager = GameManager()

# Initialize session state
if 'starting_11' not in st.session_state:
    st.session_state.starting_11 = []
if 'match_result' not in st.session_state:
    st.session_state.match_result = None
if 'game_week' not in st.session_state:
    st.session_state.game_week = 1
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'wins' not in st.session_state:
    st.session_state.wins = 0
if 'losses' not in st.session_state:
    st.session_state.losses = 0
if 'draws' not in st.session_state:
    st.session_state.draws = 0
if 'formation' not in st.session_state:
    st.session_state.formation = "4-3-3"
if 'match_events' not in st.session_state:
    st.session_state.match_events = []
if 'player_stats' not in st.session_state:
    st.session_state.player_stats = {
        player: {
            'goals': 0,
            'assists': 0,
            'clean_sheets': 0,
            'yellow_cards': 0,
            'red_cards': 0,
            'minutes_played': 0,
            'passes_completed': 0,
            'passes_attempted': 0,
            'tackles_won': 0,
            'tackles_attempted': 0,
            'shots_on_target': 0,
            'shots_attempted': 0,
            'saves': 0,
            'injury_status': 0,  # 0: healthy, 1-3: minor, 4-6: major, 7+: out
            'match_rating': 0,
            'form_momentum': 0  # -5 to +5
        } for player in player_roster.keys()
    }

def update_player_form():
    for player in player_roster:
        # Random form fluctuation between -5 and +5
        form_change = random.randint(-5, 5)
        player_roster[player]['form'] = max(0, min(100, player_roster[player]['form'] + form_change))
        # Stamina recovery
        player_roster[player]['stamina'] = min(100, player_roster[player]['stamina'] + 10)

def calculate_player_performance(player, position, team_rating, opponent_rating):
    """Calculate detailed player performance based on various factors"""
    base_rating = player_roster[player]['rating']
    form = player_roster[player]['form'] / 100
    stamina = player_roster[player]['stamina'] / 100
    momentum = st.session_state.player_stats[player]['form_momentum'] / 10
    
    # Position-specific modifiers
    position_modifiers = {
        'GK': {'defense': 1.2, 'attack': 0.3},
        'DEF': {'defense': 1.1, 'attack': 0.5},
        'MID': {'defense': 0.8, 'attack': 0.8},
        'FWD': {'defense': 0.4, 'attack': 1.2}
    }
    
    # Calculate performance factors
    performance = {
        'defense': base_rating * form * stamina * (1 + momentum) * position_modifiers[position]['defense'],
        'attack': base_rating * form * stamina * (1 + momentum) * position_modifiers[position]['attack'],
        'overall': base_rating * form * stamina * (1 + momentum)
    }
    
    # Adjust for team and opponent ratings
    team_factor = team_rating / 100
    opponent_factor = opponent_rating / 100
    
    performance['defense'] *= (1 + (team_factor - opponent_factor))
    performance['attack'] *= (1 + (team_factor - opponent_factor))
    
    return performance

def generate_match_events(team_performance, opponent_performance, minute):
    """Generate realistic match events based on team performances"""
    events = []
    
    # Calculate event probabilities based on team performances
    attack_probability = team_performance['attack'] / 100
    defense_probability = team_performance['defense'] / 100
    
    # Generate events for this minute
    if random.random() < attack_probability * 0.1:  # 10% of attack probability
        event_type = random.choices(
            list(MATCH_EVENTS.keys()),
            weights=[MATCH_EVENTS[e]['probability'] for e in MATCH_EVENTS.keys()]
        )[0]
        
        if event_type == "GOAL" and random.random() < attack_probability * 0.3:
            events.append({
                'minute': minute,
                'type': event_type,
                'description': f"{minute}' - {MATCH_EVENTS[event_type]['description']}",
                'team': 'Barcelona'
            })
    
    return events

def simulate_match(selected_players):
    if len(selected_players) != 11:
        return None
    
    # Calculate team rating considering form, stamina, and formation
    team_rating = sum(
        (player_roster[player]['rating'] * 
         (player_roster[player]['form'] / 100) * 
         (player_roster[player]['stamina'] / 100))
        for player in selected_players
    ) / 11
    
    # Generate opponent rating (80-95 range)
    opponent_rating = random.randint(80, 95)
    
    # Initialize match variables
    barca_score = 0
    opponent_score = 0
    st.session_state.match_events = []
    
    # Simulate match minute by minute
    for minute in range(1, 91):
        # Calculate current team performance
        team_performance = {
            'attack': team_rating * (1 - (minute / 90) * 0.2),  # Fatigue factor
            'defense': team_rating * (1 - (minute / 90) * 0.15)
        }
        
        opponent_performance = {
            'attack': opponent_rating * (1 - (minute / 90) * 0.2),
            'defense': opponent_rating * (1 - (minute / 90) * 0.15)
        }
        
        # Generate events for this minute
        events = generate_match_events(team_performance, opponent_performance, minute)
        st.session_state.match_events.extend(events)
        
        # Update score based on events
        for event in events:
            if event['type'] == "GOAL":
                if event['team'] == 'Barcelona':
                    barca_score += 1
                else:
                    opponent_score += 1
    
    # Generate detailed match statistics
    generate_match_stats(selected_players, barca_score, opponent_score)
    
    # Update player stats and form
    for player in selected_players:
        performance = calculate_player_performance(
            player, 
            player_roster[player]['position'],
            team_rating,
            opponent_rating
        )
        
        # Update player stats
        player_roster[player]['stamina'] = max(0, player_roster[player]['stamina'] - 10)
        st.session_state.player_stats[player]['match_rating'] = performance['overall']
        
        # Update form based on performance
        form_change = (performance['overall'] - 70) / 10  # Base form change
        if barca_score > opponent_score:
            form_change += 2  # Bonus for winning
        elif barca_score < opponent_score:
            form_change -= 1  # Penalty for losing
        
        player_roster[player]['form'] = max(0, min(100, 
            player_roster[player]['form'] + form_change))
        
        # Update form momentum
        st.session_state.player_stats[player]['form_momentum'] = max(-5, min(5,
            st.session_state.player_stats[player]['form_momentum'] + form_change))
    
    # Update game stats
    if barca_score > opponent_score:
        st.session_state.wins += 1
        st.session_state.points += 3
    elif barca_score < opponent_score:
        st.session_state.losses += 1
    else:
        st.session_state.draws += 1
        st.session_state.points += 1
    
    st.session_state.game_week += 1
    update_player_form()
    
    return barca_score, opponent_score

def generate_match_stats(selected_players, barca_score, opp_score):
    """Generate detailed match statistics for each player"""
    for player in selected_players:
        stats = st.session_state.player_stats[player]
        position = player_roster[player]['position']
        performance = calculate_player_performance(
            player,
            position,
            sum(player_roster[p]['rating'] for p in selected_players) / 11,
            random.randint(80, 95)  # Opponent rating
        )
        
        # Update minutes played
        stats['minutes_played'] += 90
        
        # Generate position-specific stats based on performance
        if position == 'GK':
            if opp_score == 0:
                stats['clean_sheets'] += 1
            # Saves based on performance
            stats['saves'] += int(performance['defense'] / 20)  # More saves for better performance
            stats['passes_completed'] += random.randint(15, 25)
            stats['passes_attempted'] += random.randint(20, 30)
        
        elif position == 'DEF':
            if opp_score == 0:
                stats['clean_sheets'] += 1
            # Defensive actions based on performance
            stats['tackles_won'] += int(performance['defense'] / 25)
            stats['tackles_attempted'] += int(performance['defense'] / 20)
            stats['passes_completed'] += int(performance['overall'] / 3)
            stats['passes_attempted'] += int(performance['overall'] / 2.5)
            # Defenders can score too
            if random.random() < (performance['attack'] / 1000):  # Better attack = more goals
                stats['goals'] += 1
        
        elif position == 'MID':
            # Midfield actions based on performance
            stats['passes_completed'] += int(performance['overall'] / 2)
            stats['passes_attempted'] += int(performance['overall'] / 1.8)
            stats['tackles_won'] += int(performance['defense'] / 30)
            stats['tackles_attempted'] += int(performance['defense'] / 25)
            # Midfielders can score and assist
            if random.random() < (performance['attack'] / 800):  # Better attack = more goals
                stats['goals'] += 1
            if random.random() < (performance['attack'] / 600):  # Better attack = more assists
                stats['assists'] += 1
        
        elif position == 'FWD':
            # Forward actions based on performance
            stats['shots_on_target'] += int(performance['attack'] / 25)
            stats['shots_attempted'] += int(performance['attack'] / 20)
            stats['passes_completed'] += int(performance['overall'] / 3.5)
            stats['passes_attempted'] += int(performance['overall'] / 3)
            # Forwards have higher chance to score
            if random.random() < (performance['attack'] / 500):  # Better attack = more goals
                stats['goals'] += 1
            if random.random() < (performance['attack'] / 700):  # Better attack = more assists
                stats['assists'] += 1
        
        # Cards based on performance (better performance = less cards)
        if random.random() < (0.1 * (1 - performance['overall'] / 100)):  # Worse performance = more cards
            stats['yellow_cards'] += 1
        if random.random() < (0.02 * (1 - performance['overall'] / 100)):
            stats['red_cards'] += 1

def display_squad():
    st.title("FC Barcelona Squad")
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        position_filter = st.multiselect(
            "Filter by Position",
            ["GK", "DEF", "MID", "FWD"],
            default=["GK", "DEF", "MID", "FWD"]
        )
    with col2:
        rating_filter = st.slider("Minimum Rating", 70, 99, 70)
    
    # Convert roster to DataFrame
    squad_data = []
    for name, stats in player_roster.items():
        if stats['position'] in position_filter and stats['rating'] >= rating_filter:
            squad_data.append({
                'Name': name,
                'Position': stats['position'],
                'Rating': stats['rating'],
                'Stamina': stats['stamina'],
                'Form': stats['form']
            })
    
    df = pd.DataFrame(squad_data)
    df = df.sort_values(['Position', 'Rating'], ascending=[True, False])
    
    # Display as a styled table
    st.dataframe(
        df.style.background_gradient(cmap='Blues', subset=['Rating', 'Stamina', 'Form']),
        use_container_width=True
    )

def display_selection():
    st.title("Select Starting 11")
    
    # Formation selection
    st.subheader("Select Formation")
    formation = st.selectbox(
        "Choose your formation",
        list(FORMATIONS.keys()),
        index=list(FORMATIONS.keys()).index(st.session_state.formation)
    )
    st.session_state.formation = formation
    
    # Display formation requirements
    st.info(f"Required players: {FORMATIONS[formation]}")
    
    # Group players by position
    positions = {
        'GK': [],
        'DEF': [],
        'MID': [],
        'FWD': []
    }
    
    for name, stats in player_roster.items():
        positions[stats['position']].append(name)
    
    # Create columns for each position
    cols = st.columns(4)
    
    # Display players by position
    for i, (pos, players) in enumerate(positions.items()):
        with cols[i]:
            st.subheader(f"{pos} ({FORMATIONS[formation][pos]} required)")
            for player in sorted(players, key=lambda x: player_roster[x]['rating'], reverse=True):
                stats = player_roster[player]
                st.markdown(f"""
                    <div class="player-stats">
                        <strong>{player}</strong><br>
                        Rating: {stats['rating']} | Stamina: {stats['stamina']}% | Form: {stats['form']}%
                    </div>
                """, unsafe_allow_html=True)
                if st.checkbox(
                    f"Select {player}",
                    key=player,
                    value=player in st.session_state.starting_11
                ):
                    if player not in st.session_state.starting_11:
                        # Check if we can add more players of this position
                        current_pos_count = sum(1 for p in st.session_state.starting_11 
                                             if player_roster[p]['position'] == pos)
                        if current_pos_count < FORMATIONS[formation][pos]:
                            st.session_state.starting_11.append(player)
                        else:
                            st.warning(f"Maximum {FORMATIONS[formation][pos]} {pos} players allowed")
                else:
                    if player in st.session_state.starting_11:
                        st.session_state.starting_11.remove(player)
    
    # Show selection status
    pos_counts = {pos: 0 for pos in positions.keys()}
    for player in st.session_state.starting_11:
        pos_counts[player_roster[player]['position']] += 1
    
    status_text = "Selection Status:\n"
    for pos, count in pos_counts.items():
        status_text += f"{pos}: {count}/{FORMATIONS[formation][pos]}\n"
    
    st.info(status_text)
    
    # Show selected players
    if st.session_state.starting_11:
        st.subheader("Your Starting 11")
        selected_df = pd.DataFrame([
            {
                'Player': player,
                'Position': player_roster[player]['position'],
                'Rating': player_roster[player]['rating'],
                'Stamina': player_roster[player]['stamina'],
                'Form': player_roster[player]['form']
            }
            for player in st.session_state.starting_11
        ])
        st.dataframe(selected_df.style.background_gradient(cmap='Blues', subset=['Rating', 'Stamina', 'Form']))

def display_match_result():
    st.title("Match Result")
    
    if st.session_state.match_result:
        competition, opponent, barca_score, opp_score = st.session_state.match_result
        st.markdown(f"""
            <div class="match-result">
                {competition.value}<br>
                Barcelona {barca_score} - {opp_score} {opponent}
            </div>
        """, unsafe_allow_html=True)
        
        if barca_score > opp_score:
            st.success("Victory! 🎉")
        elif barca_score < opp_score:
            st.error("Defeat 😢")
        else:
            st.warning("Draw 🤝")
        
        # Display match events
        st.subheader("Match Events")
        for event in st.session_state.match_events:
            st.markdown(f"**{event['minute']}'** - {event['description']}")
        
        # Display player ratings
        st.subheader("Player Ratings")
        ratings_data = pd.DataFrame([
            {
                'Player': player,
                'Position': player_roster[player]['position'],
                'Rating': round(st.session_state.player_stats[player]['match_rating'], 1),
                'Form': player_roster[player]['form']
            }
            for player in st.session_state.starting_11
        ])
        st.dataframe(
            ratings_data.sort_values('Rating', ascending=False)
            .style.background_gradient(cmap='RdYlGn', subset=['Rating', 'Form'])
        )

def display_stats():
    st.title("Season Statistics")
    
    # Team Overview
    st.subheader("Team Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Game Week", st.session_state.game_week)
    with col2:
        st.metric("Points", st.session_state.points)
    with col3:
        st.metric("Wins", st.session_state.wins)
    with col4:
        st.metric("Losses", st.session_state.losses)
    
    # Player Statistics
    st.subheader("Player Statistics")
    
    # Create tabs for different stat categories
    tab1, tab2, tab3, tab4 = st.tabs(["Attack", "Defense", "Passing", "Cards"])
    
    with tab1:
        # Attack stats
        attack_data = pd.DataFrame([
            {
                'Player': player,
                'Goals': stats['goals'],
                'Assists': stats['assists'],
                'Shots on Target': stats['shots_on_target'],
                'Shots Attempted': stats['shots_attempted']
            }
            for player, stats in st.session_state.player_stats.items()
        ])
        st.dataframe(
            attack_data.sort_values('Goals', ascending=False)
            .style.background_gradient(cmap='Reds', subset=['Goals', 'Assists', 'Shots on Target'])
        )
    
    with tab2:
        # Defense stats
        defense_data = pd.DataFrame([
            {
                'Player': player,
                'Clean Sheets': stats['clean_sheets'],
                'Tackles Won': stats['tackles_won'],
                'Tackle Success %': round(stats['tackles_won'] / max(1, stats['tackles_attempted']) * 100, 1),
                'Saves': stats['saves']
            }
            for player, stats in st.session_state.player_stats.items()
        ])
        st.dataframe(
            defense_data.sort_values('Clean Sheets', ascending=False)
            .style.background_gradient(cmap='Blues', subset=['Clean Sheets', 'Tackles Won', 'Saves'])
        )
    
    with tab3:
        # Passing stats
        passing_data = pd.DataFrame([
            {
                'Player': player,
                'Passes Completed': stats['passes_completed'],
                'Passes Attempted': stats['passes_attempted'],
                'Pass Accuracy %': round(stats['passes_completed'] / max(1, stats['passes_attempted']) * 100, 1)
            }
            for player, stats in st.session_state.player_stats.items()
        ])
        st.dataframe(
            passing_data.sort_values('Passes Completed', ascending=False)
            .style.background_gradient(cmap='Greens', subset=['Passes Completed', 'Pass Accuracy %'])
        )
    
    with tab4:
        # Cards stats
        cards_data = pd.DataFrame([
            {
                'Player': player,
                'Yellow Cards': stats['yellow_cards'],
                'Red Cards': stats['red_cards']
            }
            for player, stats in st.session_state.player_stats.items()
        ])
        st.dataframe(
            cards_data.sort_values(['Red Cards', 'Yellow Cards'], ascending=[False, False])
            .style.background_gradient(cmap='Oranges', subset=['Yellow Cards', 'Red Cards'])
        )
    
    # Minutes Played
    st.subheader("Minutes Played")
    minutes_data = pd.DataFrame([
        {'Player': player, 'Minutes': stats['minutes_played']}
        for player, stats in st.session_state.player_stats.items()
    ])
    st.bar_chart(minutes_data.set_index('Player'))

def display_standings():
    """Display current standings for all competitions"""
    st.title("Competition Standings")
    
    # Create tabs for each competition
    tabs = st.tabs([comp.value for comp in Competition])
    
    for idx, tab in enumerate(tabs):
        with tab:
            st.markdown(f"<div class='standings-table'>", unsafe_allow_html=True)
            
            # Get the current competition
            competition = list(Competition)[idx]
            
            # Add competition-specific information
            if competition == Competition.LA_LIGA:
                st.subheader("La Liga 2024-25")
                st.info("38 games per team - 3 points for win, 1 for draw")
                st.markdown("**Current Game Week:** " + str(st.session_state.game_week))
            elif competition == Competition.CHAMPIONS_LEAGUE:
                st.subheader("UEFA Champions League 2024-25")
                st.info("New Format: 8 games in league phase, followed by knockout rounds")
                st.markdown("**Current Stage:** League Phase")
            elif competition == Competition.COPA_DEL_REY:
                st.subheader("Copa del Rey 2024-25")
                st.info("Single-elimination tournament - Round of 32")
                st.markdown("**Current Stage:** Round of 32")
            else:  # Supercopa
                st.subheader("Supercopa de España 2024-25")
                st.info("Four-team tournament - Semi-finals and Final")
                st.markdown("**Current Stage:** Semi-finals")
            
            # Display the standings as a DataFrame
            df = st.session_state.game_manager.get_standings_data(competition)
            st.dataframe(
                df.style.background_gradient(cmap='Blues', subset=['Points', 'Goal Difference']),
                use_container_width=True
            )
            
            # Add competition-specific notes
            if competition == Competition.LA_LIGA:
                st.markdown("""
                    **Promotion/Relegation:**
                    - Top 4: Champions League qualification
                    - 5th-6th: Europa League qualification
                    - Bottom 3: Relegation to Segunda División
                """)
            elif competition == Competition.CHAMPIONS_LEAGUE:
                st.markdown("""
                    **Qualification:**
                    - Top 8: Direct qualification to Round of 16
                    - 9th-24th: Play-off round
                    - Bottom 12: Eliminated
                """)
            elif competition == Competition.COPA_DEL_REY:
                st.markdown("""
                    **Tournament Format:**
                    - Single-elimination matches
                    - Two-legged ties until semi-finals
                    - Single match final
                """)
            else:  # Supercopa
                st.markdown("""
                    **Tournament Format:**
                    - Semi-finals: La Liga champions vs Copa del Rey runners-up
                    - Semi-finals: Copa del Rey winners vs La Liga runners-up
                    - Single match final
                """)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add a refresh button for each competition
            if st.button(f"Refresh {competition.value} Standings", key=f"refresh_{competition.value}"):
                st.rerun()

# Main app
st.title("FC Barcelona Manager")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Squad", "Select Team", "Play Match", "Statistics", "Standings"])

if page == "Squad":
    display_squad()
elif page == "Select Team":
    display_selection()
elif page == "Play Match":
    if len(st.session_state.starting_11) == 11:
        st.subheader(f"Game Week {st.session_state.game_week}")
        
        # Competition selection
        competition = st.selectbox(
            "Select Competition",
            [comp.value for comp in Competition]
        )
        competition = Competition(competition)
        
        # Get available opponents for the selected competition
        opponents = [team for team in st.session_state.game_manager.standings[competition].keys() 
                    if team != "FC Barcelona"]
        
        # Opponent selection
        opponent = st.selectbox(
            "Select Opponent",
            opponents
        )
        
        if st.button("Play Match"):
            with st.spinner("Simulating match..."):
                time.sleep(2)  # Add some drama
                barca_score, opp_score = st.session_state.game_manager.simulate_match(
                    competition, "FC Barcelona", opponent
                )
                st.session_state.match_result = (competition, opponent, barca_score, opp_score)
        
        if st.session_state.match_result:
            display_match_result()
    else:
        st.error("Please select exactly 11 players first!")
elif page == "Statistics":
    display_stats()
elif page == "Standings":
    display_standings() 