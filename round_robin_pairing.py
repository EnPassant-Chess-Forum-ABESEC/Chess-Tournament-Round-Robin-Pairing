import csv
import os
from typing import List, Tuple, Set, Dict

class Player:
    def __init__(self, player_id, name, rating):
        self.id = player_id
        self.name = name
        self.rating = rating
        self.score = 0.0
        self.opponents = []
        self.opponent_results = []
        self.colors = []
        self.wins = 0
        self.losses = 0
        self.draws = 0

class RoundRobinTournament:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.main_file = csv_file.replace('.csv', '_MAIN.csv')
        self.players = {}
        self.rounds_data = {}
        self.current_round = 0
        self.total_rounds = 0
    
    def load_from_main_csv(self):
        """Load players and all previous round data from MAIN CSV"""
        try:
            with open(self.main_file, 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                
                # First pass: collect all unique players
                player_ids_seen = set()
                for row in rows:
                    try:
                        player_id = int(row['ID'])
                        if player_id not in player_ids_seen:
                            name = row['Name'].strip()
                            rating = int(row['Rating'])
                            self.players[player_id] = Player(player_id, name, rating)
                            player_ids_seen.add(player_id)
                    except (ValueError, KeyError):
                        pass
                
                # Second pass: collect all round data
                for row in rows:
                    try:
                        player_id = int(row['ID'])
                    except (ValueError, KeyError):
                        continue
                    
                    # Get player's total score from MAIN file
                    try:
                        self.players[player_id].score = float(row.get('Total_Score', 0))
                        self.players[player_id].wins = int(row.get('Wins', 0))
                        self.players[player_id].losses = int(row.get('Losses', 0))
                        self.players[player_id].draws = int(row.get('Draws', 0))
                    except (ValueError, TypeError):
                        self.players[player_id].score = 0.0
                    
                    # Process all round columns
                    round_num = 1
                    while True:
                        white_col = f'Round_{round_num}_White'
                        black_col = f'Round_{round_num}_Black'
                        result_col = f'Round_{round_num}_Result'
                        
                        if white_col not in row or row[white_col].strip() == '':
                            break
                        
                        try:
                            white_id = int(row[white_col])
                            black_id = int(row[black_col])
                            
                            if round_num not in self.rounds_data:
                                self.rounds_data[round_num] = {}
                            
                            match_key = (min(white_id, black_id), max(white_id, black_id))
                            
                            if match_key not in self.rounds_data[round_num]:
                                self.rounds_data[round_num][match_key] = {
                                    'white_id': white_id,
                                    'black_id': black_id,
                                    'result': None
                                }
                            
                            result = row[result_col].strip()
                            if result and result != '':
                                try:
                                    result_value = float(result)
                                    self.rounds_data[round_num][match_key]['result'] = result_value
                                except ValueError:
                                    pass
                            
                            round_num += 1
                        except (ValueError, KeyError):
                            break
            
            print(f"✓ Loaded {len(self.players)} players from {self.main_file}")
            
            # Convert rounds_data to list format
            for round_num in self.rounds_data:
                self.rounds_data[round_num] = list(self.rounds_data[round_num].values())
            
            self.current_round = len(self.rounds_data)
            print(f"✓ Previous rounds completed: {self.current_round}")
            
        except FileNotFoundError:
            print(f"Note: {self.main_file} not found. This is a new tournament.")
    
    def calculate_total_rounds(self):
        """Calculate total number of rounds needed for round robin"""
        num_players = len(self.players)
        if num_players % 2 == 0:
            self.total_rounds = num_players - 1
        else:
            self.total_rounds = num_players
        return self.total_rounds
    
    def load_round_results(self, round_num):
        """Load results from a specific round results file"""
        round_file = self.csv_file.replace('.csv', f'_ROUND_{round_num}_RESULTS.csv')
        
        if not os.path.exists(round_file):
            print(f"Note: Results file not found: {round_file}")
            return False
        
        try:
            with open(round_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        white_id = int(row['White_ID'])
                        black_id = int(row['Black_ID'])
                        result = row['White_Result'].strip()
                        
                        if result == '':
                            continue
                        
                        result_value = float(result)
                        
                        # Find and update the match in rounds_data
                        if round_num in self.rounds_data:
                            for match in self.rounds_data[round_num]:
                                if match['white_id'] == white_id and match['black_id'] == black_id:
                                    match['result'] = result_value
                                    break
                    except (ValueError, KeyError):
                        continue
            
            print(f"✓ Loaded results from {round_file}")
            self._calculate_scores()
            return True
        except Exception as e:
            print(f"Error reading results file: {e}")
            return False
    
    def _calculate_scores(self):
        """Calculate scores from all completed rounds"""
        for player in self.players.values():
            player.score = 0.0
            player.opponents = []
            player.opponent_results = []
            player.colors = []
            player.wins = 0
            player.losses = 0
            player.draws = 0
        
        for round_num in sorted(self.rounds_data.keys()):
            for match in self.rounds_data[round_num]:
                white_id = match['white_id']
                black_id = match['black_id']
                result = match.get('result')
                
                if result is None:
                    continue
                
                if white_id in self.players and black_id in self.players:
                    self.players[white_id].score += result
                    self.players[black_id].score += (1.0 - result)
                    
                    # Track wins/draws/losses
                    if result == 1.0:
                        self.players[white_id].wins += 1
                        self.players[black_id].losses += 1
                    elif result == 0.5:
                        self.players[white_id].draws += 1
                        self.players[black_id].draws += 1
                    else:
                        self.players[white_id].losses += 1
                        self.players[black_id].wins += 1
                    
                    self.players[white_id].opponents.append(black_id)
                    self.players[black_id].opponents.append(white_id)
                    
                    self.players[white_id].opponent_results.append(result)
                    self.players[black_id].opponent_results.append(1.0 - result)
                    
                    self.players[white_id].colors.append('W')
                    self.players[black_id].colors.append('B')
    
    def display_players(self):
        """Display all players"""
        print("\n" + "="*50)
        print("PLAYERS LIST")
        print("="*50)
        print(f"{'ID':<5} {'Name':<20} {'Rating':<10}")
        print("-"*50)
        for pid in sorted(self.players.keys()):
            p = self.players[pid]
            print(f"{p.id:<5} {p.name:<20} {p.rating:<10}")
    
    def determine_color(self, p1, p2):
        """Determine who plays white based on color balance"""
        p1_whites = p1.colors.count('W')
        p1_blacks = p1.colors.count('B')
        p2_whites = p2.colors.count('W')
        p2_blacks = p2.colors.count('B')
        
        p1_balance = p1_whites - p1_blacks
        p2_balance = p2_whites - p2_blacks
        
        if p1_balance < p2_balance:
            return p1.id, p2.id
        elif p2_balance < p1_balance:
            return p2.id, p1.id
        else:
            if p1.rating >= p2.rating:
                return p1.id, p2.id
            else:
                return p2.id, p1.id
    
    def generate_round_robin_pairings(self):
        """Generate all round robin pairings using circle method"""
        player_list = sorted(self.players.keys())
        num_players = len(player_list)
        
        # Add bye player if odd number
        if num_players % 2 == 1:
            player_list.append(None)
            num_players += 1
        
        all_pairings = []
        
        # Circle algorithm for round robin
        for round_num in range(num_players - 1):
            round_pairings = []
            
            for i in range(num_players // 2):
                p1 = player_list[i]
                p2 = player_list[num_players - 1 - i]
                
                if p1 is not None and p2 is not None:
                    round_pairings.append((p1, p2))
            
            all_pairings.append(round_pairings)
            
            # Rotate for next round (keep first fixed)
            player_list = [player_list[0]] + player_list[-1:] + player_list[1:-1]
        
        return all_pairings
    
    def generate_next_round(self):
        """Generate pairings for the next round"""
        if self.current_round == 0:
            # First time: generate all pairings
            all_pairings = self.generate_round_robin_pairings()
            for i, pairings in enumerate(all_pairings, 1):
                self.rounds_data[i] = []
                for p1_id, p2_id in pairings:
                    white_id, black_id = self.determine_color(
                        self.players[p1_id], self.players[p2_id]
                    )
                    self.rounds_data[i].append({
                        'white_id': white_id,
                        'black_id': black_id,
                        'result': None
                    })
            
            self.total_rounds = len(self.rounds_data)
        
        round_num = self.current_round + 1
        
        if round_num > self.total_rounds:
            print(f"Tournament is complete! All {self.total_rounds} rounds have been scheduled.")
            return None, None
        
        pairings = []
        for match in self.rounds_data[round_num]:
            white_id = match['white_id']
            black_id = match['black_id']
            white_player = self.players[white_id]
            black_player = self.players[black_id]
            
            pairings.append({
                'white_id': white_id,
                'white_name': white_player.name,
                'white_rating': white_player.rating,
                'black_id': black_id,
                'black_name': black_player.name,
                'black_rating': black_player.rating
            })
        
        return round_num, pairings
    
    def display_round(self, round_num):
        """Display pairings for a specific round"""
        if round_num not in self.rounds_data:
            print("Invalid round number!")
            return
        
        matches = self.rounds_data[round_num]
        print("\n" + "="*90)
        print(f"ROUND {round_num} PAIRINGS")
        print("="*90)
        print(f"{'M#':<4} {'White (ID)':<25} {'Rating':<8} | {'Black (ID)':<25} {'Rating':<8}")
        print("-"*90)
        
        for i, match in enumerate(matches):
            white_id = match['white_id']
            black_id = match['black_id']
            white_player = self.players[white_id]
            black_player = self.players[black_id]
            
            white_display = f"{white_player.name} ({white_id})"
            black_display = f"{black_player.name} ({black_id})"
            
            print(f"{i+1:<4} {white_display:<25} {white_player.rating:<8} | "
                  f"{black_display:<25} {black_player.rating:<8}")
    
    def display_standings(self):
        """Display current tournament standings"""
        print("\n" + "="*110)
        print("CURRENT STANDINGS")
        print("="*110)
        print(f"{'Rank':<6} {'ID':<6} {'Name':<20} {'Rating':<8} {'Score':<8} {'W':<5} {'D':<5} {'L':<5} {'Rounds':<8}")
        print("-"*110)
        
        sorted_players = sorted(self.players.values(), 
                               key=lambda p: (-p.score, -p.wins, -p.rating))
        
        for rank, player in enumerate(sorted_players, 1):
            rounds_played = player.wins + player.losses + player.draws
            print(f"{rank:<6} {player.id:<6} {player.name:<20} {player.rating:<8} "
                  f"{player.score:<8.1f} {player.wins:<5} {player.draws:<5} {player.losses:<5} {rounds_played:<8}")
    
    def create_round_results_template(self, round_num, pairings):
        """Create a template file for entering round results"""
        round_file = self.csv_file.replace('.csv', f'_ROUND_{round_num}_RESULTS.csv')
        
        try:
            with open(round_file, 'w', newline='') as file:
                headers = ['Match_No', 'White_ID', 'White_Name', 'White_Rating', 
                          'Black_ID', 'Black_Name', 'Black_Rating', 'White_Result']
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                
                for i, pairing in enumerate(pairings):
                    writer.writerow({
                        'Match_No': i + 1,
                        'White_ID': pairing['white_id'],
                        'White_Name': pairing['white_name'],
                        'White_Rating': pairing['white_rating'],
                        'Black_ID': pairing['black_id'],
                        'Black_Name': pairing['black_name'],
                        'Black_Rating': pairing['black_rating'],
                        'White_Result': ''
                    })
            
            print(f"✓ Results template created: {round_file}")
            return round_file
        except Exception as e:
            print(f"Error creating results template: {e}")
            return None
    
    def save_main_csv(self):
        """Save main tournament data with all rounds"""
        try:
            with open(self.main_file, 'w', newline='') as file:
                # Prepare header
                headers = ['ID', 'Name', 'Rating', 'Total_Score', 'Wins', 'Draws', 'Losses']
                for round_num in sorted(self.rounds_data.keys()):
                    headers.append(f'Round_{round_num}_White')
                    headers.append(f'Round_{round_num}_Black')
                    headers.append(f'Round_{round_num}_Result')
                
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                
                # Write player data sorted by standings
                sorted_players = sorted(self.players.values(), 
                                      key=lambda p: (-p.score, -p.wins, -p.rating))
                
                for player in sorted_players:
                    pid = player.id
                    row = {
                        'ID': player.id,
                        'Name': player.name,
                        'Rating': player.rating,
                        'Total_Score': f"{player.score:.1f}",
                        'Wins': player.wins,
                        'Draws': player.draws,
                        'Losses': player.losses
                    }
                    
                    for round_num in sorted(self.rounds_data.keys()):
                        # Find which match this player was in for this round
                        found = False
                        for match in self.rounds_data[round_num]:
                            if match['white_id'] == pid or match['black_id'] == pid:
                                row[f'Round_{round_num}_White'] = match['white_id']
                                row[f'Round_{round_num}_Black'] = match['black_id']
                                
                                result = match.get('result')
                                if match['white_id'] == pid:
                                    row[f'Round_{round_num}_Result'] = result if result is not None else ''
                                else:
                                    if result is not None:
                                        row[f'Round_{round_num}_Result'] = 1.0 - result
                                    else:
                                        row[f'Round_{round_num}_Result'] = ''
                                
                                found = True
                                break
                        
                        if not found:
                            row[f'Round_{round_num}_White'] = ''
                            row[f'Round_{round_num}_Black'] = ''
                            row[f'Round_{round_num}_Result'] = ''
                    
                    writer.writerow(row)
            
            print(f"✓ Main file updated: {self.main_file}")
        except Exception as e:
            print(f"Error saving main CSV: {e}")

def create_blank_csv(csv_file, num_players):
    """Create a blank CSV template with column headers for players to fill"""
    try:
        headers = ['ID', 'Name', 'Rating']
        
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            
            # Add blank rows for players
            for i in range(num_players):
                writer.writerow({'ID': '', 'Name': '', 'Rating': ''})
        
        print(f"✓ Blank CSV template created: {csv_file}")
        print(f"✓ Open {csv_file} in Excel/LibreOffice and fill in player details")
        print(f"✓ Columns: ID, Name, Rating")
        print(f"✓ Template has {num_players} blank rows ready for data entry")
        return True
    except Exception as e:
        print(f"Error creating CSV: {e}")
        return False

def main():
    print("="*70)
    print("ROUND ROBIN TOURNAMENT PAIRING SYSTEM")
    print("="*70)
    
    print("\n1. Create blank CSV template for new tournament")
    print("2. Run tournament with existing CSV file")
    
    choice = input("\nChoice (1 or 2): ").strip()
    
    if choice == '1':
        csv_file = input("Enter CSV filename to create (e.g., tournament.csv): ").strip()
        
        if os.path.exists(csv_file):
            print(f"Warning: {csv_file} already exists!")
            overwrite = input("Overwrite? (y/n): ").strip().lower()
            if overwrite != 'y':
                return
        
        while True:
            try:
                num_players = int(input("Enter number of players: "))
                if num_players > 0:
                    break
                print("Number of players must be positive!")
            except ValueError:
                print("Please enter a valid number!")
        
        if create_blank_csv(csv_file, num_players):
            print("\n" + "="*70)
            print("Template created successfully!")
            print("Edit the CSV file and fill in player details, then run the program again")
            print("="*70)
        return
    
    elif choice == '2':
        csv_file = input("\nEnter CSV filename (e.g., tournament.csv): ").strip()
    else:
        print("Invalid choice!")
        return
    
    tournament = RoundRobinTournament(csv_file)
    
    if os.path.exists(csv_file):
        # Load initial players from the input file
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        player_id = int(row['ID'])
                        name = row['Name'].strip()
                        rating = int(row['Rating'])
                        if player_id and name and rating:
                            tournament.players[player_id] = Player(player_id, name, rating)
                    except (ValueError, KeyError):
                        continue
            
            # Load previous rounds from MAIN file if it exists
            if os.path.exists(tournament.main_file):
                tournament.load_from_main_csv()
                
                # Load results from the latest round
                if tournament.current_round > 0:
                    tournament.load_round_results(tournament.current_round)
        
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return
    else:
        print(f"Error: File {csv_file} not found!")
        return
    
    tournament.display_players()
    tournament.calculate_total_rounds()
    print(f"\nTotal rounds needed: {tournament.total_rounds}")
    tournament.display_standings()
    
    print("\n" + "="*70)
    print("GENERATING NEXT ROUND PAIRINGS...")
    print("="*70)
    
    round_num, pairings = tournament.generate_next_round()
    
    if round_num is None:
        print("\n✓ Tournament is already complete!")
        return
    
    tournament.display_round(round_num)
    
    # Create round results template
    results_file = tournament.create_round_results_template(round_num, pairings)
    
    # Save main file
    tournament.save_main_csv()
    
    print("\n" + "="*70)
    print(f"✓ Round {round_num} of {tournament.total_rounds} pairings generated!")
    print("="*70)
    print("\nNEXT STEPS:")
    print("-" * 70)
    print(f"1. Open '{results_file}'")
    print("2. Enter match results in 'White_Result' column:")
    print("   - 1 = White wins")
    print("   - 0.5 = Draw")
    print("   - 0 = Black wins")
    print(f"3. Save the results file")
    print(f"4. Run the program again to generate Round {round_num + 1}")
    print("-" * 70)
    print(f"✓ Main tournament file: {tournament.main_file}")
    print("="*70)

if __name__ == "__main__":
    main()