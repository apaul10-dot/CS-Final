import pandas as pd
import glob

# Find all players CSV files in the current directory
csv_files = sorted(glob.glob('players (*.csv'))

# Read and concatenate all CSVs
df_list = [pd.read_csv(f) for f in csv_files]
all_players = pd.concat(df_list, ignore_index=True)

# Remove duplicates based on 'info.playerid' (or fallback to 'info.name.firstname' + 'info.name.lastname')
if 'info.playerid' in all_players.columns:
    all_players = all_players.drop_duplicates(subset=['info.playerid'])
else:
    all_players = all_players.drop_duplicates(subset=['info.name.firstname', 'info.name.lastname'])

# Save to players.csv
all_players.to_csv('players.csv', index=False)

print(f"Merged {len(csv_files)} files into players.csv with {len(all_players)} unique players.") 