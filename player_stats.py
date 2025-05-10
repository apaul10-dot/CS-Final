import csv

# Example stats for players
all_stats = {
    "Goalkeepers": {
        "Marc-Andre ter Stegan": {
            "goals": 0,
            "assists": 0,
            "passes_completed": 500,
            "clean_sheets": 20
        },
        "Inaki Pena": {
            "goals": 0,
            "assists": 0,
            "passes_completed": 300,
            "clean_sheets": 10
        }
    },
    "Strikers": {
        "Robert Lewandowski": {
            "goals": 30,
            "assists": 10,
            "passes_completed": 200,
            "clean_sheets": 0
        },
        "Ferran Torres": {
            "goals": 15,
            "assists": 8,
            "passes_completed": 150,
            "clean_sheets": 0
        }
    }
}

# Write to a CSV file
with open("player_stats.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["Position", "Player", "Goals", "Assists", "Passes Completed", "Clean Sheets"])
    
    # Write the stats
    for position, players in all_stats.items():
        for player, stats in players.items():
            writer.writerow([
                position,
                player,
                stats.get("goals", 0),
                stats.get("assists", 0),
                stats.get("passes_completed", 0),
                stats.get("clean_sheets", 0)
            ])