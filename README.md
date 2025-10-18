# Round Robin Tournament Pairing System

A comprehensive Python-based application for organizing and managing round robin chess tournaments with automatic pairing generation, color balancing, and detailed standings tracking.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Getting Started](#getting-started)
5. [Workflow](#workflow)
6. [File Formats](#file-formats)
7. [Features Explained](#features-explained)
8. [FAQ](#faq)

---

## Overview

This system automates the organization of round robin chess tournaments where each player competes against every other player exactly once. It handles player registration, automatic pairing generation using the circle method algorithm, color assignment, result tracking, and standing calculations.

### Round Robin Tournament Structure

In a round robin tournament:
- Every player plays every other player exactly once
- Total rounds = n-1 (for even number of players) or n (for odd number of players)
- Total games = n × (n-1) / 2, where n = number of players

For example, an 8-player tournament requires 7 rounds with 28 total games.

---

## Features

- **Automatic Pairing Generation**: Uses the proven circle method algorithm for fair and balanced pairings
- **Color Balancing**: Intelligently assigns white and black pieces to balance color frequency and advantage
- **Player Management**: Easy player registration with ID, name, and rating
- **Comprehensive Standings**: Displays scores, wins, draws, losses, and rounds played
- **CSV-Based Tracking**: All tournament data stored in easy-to-read CSV files
- **Result Management**: Template files for easy result entry
- **Tournament Persistence**: Continue tournaments across multiple sessions
- **Flexible Player Count**: Handles both even and odd numbers of players seamlessly

---

## Installation

### Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### Setup

1. Download or clone the round robin tournament system files
2. Ensure `round_robin_tournament.py` is in your working directory
3. Open a terminal/command prompt in the directory containing the script

---

## Getting Started

### Step 1: Create a New Tournament

Run the program for the first time:

```bash
python round_robin_tournament.py
```

Select option 1 to create a new tournament:

```
================================================== =====
ROUND ROBIN TOURNAMENT PAIRING SYSTEM
==================================================== 

1. Create blank CSV template for new tournament
2. Run tournament with existing CSV file

Choice (1 or 2): 1
```

Enter a filename (e.g., `chess_tournament.csv`) and the number of players:

```
Enter CSV filename to create (e.g., tournament.csv): chess_tournament.csv
Enter number of players: 8
```

The system will create a blank template CSV file.

### Step 2: Fill in Player Details

Open the generated CSV file in Excel, Google Sheets, or LibreOffice Calc. Fill in player information:

| ID  | Name              | Rating |
|-----|-------------------|--------|
| 1   | Alice Johnson     | 1850   |
| 2   | Bob Smith         | 1720   |
| 3   | Carol White       | 1950   |
| 4   | David Brown       | 1680   |
| 5   | Eva Martinez      | 1800   |
| 6   | Frank Garcia      | 1620   |
| 7   | Grace Lee         | 1900   |
| 8   | Henry Wilson      | 1750   |

Save the file and proceed to step 3.

### Step 3: Generate Round 1 Pairings

Run the program again and select option 2:

```
Choice (1 or 2): 2
Enter CSV filename (e.g., tournament.csv): chess_tournament.csv
```

The system will:
- Load all players
- Calculate total rounds needed
- Display current standings (empty for round 1)
- Generate Round 1 pairings
- Create a results template file

### Step 4: Enter Match Results

Open the generated results file (`chess_tournament_ROUND_1_RESULTS.csv`) and enter the match results:

| Match_No | White_ID | White_Name  | White_Rating | Black_ID | Black_Name | Black_Rating | White_Result |
|----------|----------|-------------|--------------|----------|------------|--------------|--------------|
| 1        | 3        | Carol White | 1950         | 1        | Alice      | 1850         | 1            |
| 2        | 7        | Grace Lee   | 1900         | 5        | Eva        | 1800         | 0.5          |
| 3        | 2        | Bob Smith   | 1720         | 4        | David      | 1680         | 0            |
| 4        | 8        | Henry       | 1750         | 6        | Frank      | 1620         | 1            |

Result encoding:
- `1` = White wins
- `0.5` = Draw
- `0` = Black wins

### Step 5: Repeat for Next Rounds

Run the program again to:
- Load completed round results
- Update standings
- Generate next round pairings
- Create results template for the next round

Repeat until all rounds are complete.

---

## Workflow

### Tournament Flow Diagram

```
1. Create New Tournament
   └─ Generate blank CSV template
      └─ Player fills in details
         └─ Save player file

2. Generate Pairings
   └─ Load players from CSV
      └─ Calculate all round robin pairings
         └─ Generate Round 1 pairings
            └─ Create results template

3. Enter Results
   └─ Open results template
      └─ Enter match outcomes
         └─ Save results file

4. Update Tournament
   └─ Load results
      └─ Calculate standings
         └─ Generate next round pairings
            └─ Repeat steps 3-4

5. Tournament Complete
   └─ All rounds finished
      └─ Final standings displayed
         └─ Main CSV contains full tournament history
```

### Typical Tournament Timeline

For an 8-player tournament:
- **Total rounds**: 7
- **Total games**: 28
- **Games per round**: 4
- **Games per player**: 7 (one against each opponent)

---

## File Formats

### Player Input File (chess_tournament.csv)

Contains player registration information.

```csv
ID,Name,Rating
1,Alice Johnson,1850
2,Bob Smith,1720
3,Carol White,1950
```

**Fields:**
- `ID`: Unique player identifier (must be integer)
- `Name`: Player's name
- `Rating`: Player's ELO rating (integer)

### Results Template (chess_tournament_ROUND_1_RESULTS.csv)

Auto-generated template for entering match results.

```csv
Match_No,White_ID,White_Name,White_Rating,Black_ID,Black_Name,Black_Rating,White_Result
1,3,Carol White,1950,1,Alice Johnson,1850,
2,7,Grace Lee,1900,5,Eva Martinez,1800,
```

**Fields:**
- `Match_No`: Match number within the round
- `White_ID`: ID of player with white pieces
- `White_Name`: Name of white player
- `White_Rating`: Rating of white player
- `Black_ID`: ID of player with black pieces
- `Black_Name`: Name of black player
- `Black_Rating`: Rating of black player
- `White_Result`: Enter 1, 0.5, or 0 (must be filled)

### Main Tournament File (chess_tournament_MAIN.csv)

Complete tournament record with all results and standings.

```csv
ID,Name,Rating,Total_Score,Wins,Draws,Losses,Round_1_White,Round_1_Black,Round_1_Result,...
1,Alice Johnson,1850,5.5,4,3,0,1,3,0,...
3,Carol White,1950,6.0,5,1,1,3,1,1,...
```

**Fields:**
- `ID`: Player ID
- `Name`: Player name
- `Rating`: Player rating
- `Total_Score`: Current score (points earned)
- `Wins`: Number of wins
- `Draws`: Number of draws
- `Losses`: Number of losses
- `Round_X_White`: White player ID for round X
- `Round_X_Black`: Black player ID for round X
- `Round_X_Result`: Match result from player's perspective

---

## Features Explained

### Pairing Generation (Circle Method)

The circle method is a standard algorithm for round robin tournaments:

1. Arrange players in a circle
2. For each round:
   - Pair players across the circle (top with bottom, second with second-to-last, etc.)
   - Rotate all players except the first one
3. Repeat for n-1 rounds (or n for odd numbers)

This method ensures:
- Each player meets every other player exactly once
- Fairness and balance in the pairings
- Predictable, reproducible results

### Color Balancing

The system intelligently assigns white and black pieces:

1. **Balance Score**: Calculated as (White Count - Black Count)
   - Player with lower balance plays white (fewer whites recently)
   - Minimizes color imbalance across the tournament

2. **Tiebreaker**: If both players have equal balance
   - Higher rated player plays white
   - Ensures consistency in rating-based assignments

### Standings Calculation

Players are ranked by:
1. **Primary**: Total Score (points from all games)
2. **Secondary**: Number of Wins (win count)
3. **Tertiary**: Ratings (for final tiebreaking)

Score calculation:
- Win = 1 point
- Draw = 0.5 points
- Loss = 0 points

---

## FAQ

### Q: Can I add or remove players mid-tournament?

A: It's not recommended. Round robin tournaments are designed with a fixed player set. Adding players after pairings are generated can create inconsistencies. Best practice is to finalize your player list before generating Round 1.

### Q: What if a player needs to miss a round?

A: You can manually skip that matchup by not entering a result for it. However, this will create an unbalanced tournament. For best results, have all players available for all rounds.

### Q: How do I handle an odd number of players?

A: The system automatically handles this! It creates a "bye" (rest round) for each round. The bye appears as an empty slot in pairings. It's mathematically equivalent to a win for standings purposes.

### Q: Can I modify pairings after they're generated?

A: The CSV files are human-readable and editable. You can manually edit the `ROUND_X_White` and `ROUND_X_Black` columns in the main file before running the next round generation. However, this may disrupt the round robin structure.

### Q: How do I restart a tournament from scratch?

A: Delete both the original CSV file and the corresponding `_MAIN.csv` file, then run the program again to create a new tournament.

### Q: What rating system does this use?

A: The system accepts any integer rating. Common systems include ELO (chess), which typically ranges from 800-2800+, but any rating scale works.

### Q: Can I run multiple tournaments simultaneously?

A: Yes! Use different filenames (e.g., `tournament_a.csv`, `tournament_b.csv`). Each tournament will have its own separate main file and round results files.

### Q: Is there a maximum number of players?

A: No hard limit, but practical considerations apply:
- 16 players = 15 rounds (large but manageable)
- 32 players = 31 rounds (very long tournament)
- Consider splitting into sections for large groups

### Q: How are tiebreaks handled?

A: The standings display automatically sorts by score (primary), then wins (secondary), then rating (tertiary). The CSV shows exact scores for manual tiebreaking if needed.

### Q: Can I export standings to a different format?

A: The standings are shown in the console output and stored in the CSV file. You can open the CSV in any spreadsheet program and export to PDF, Excel, or other formats as needed.

---

## System Requirements

- **Python Version**: 3.6+
- **Memory**: Minimal (< 10MB for tournaments up to ~100 players)
- **Disk Space**: Minimal (< 1MB per tournament)
- **Operating System**: Windows, macOS, or Linux

## Troubleshooting

### "File not found" error

Ensure the CSV file is in the same directory as the Python script, or provide the full file path.

### Results not loading

Check that the results file has the exact name format: `filename_ROUND_X_RESULTS.csv`

### Incorrect standings

Verify all result values are entered as `1`, `0.5`, or `0`. Invalid values will be skipped.

### Tournament appears to restart

If the main file (`_MAIN.csv`) was deleted, the tournament resets. Keep backups of important tournament files.

---

## Support and Contributing

For issues or feature requests, refer to the program's console output for specific error messages. All operations log their status with ✓ (success) or Note: (informational) indicators.

---

**Version**: 1.0  
**Last Updated**: 2025