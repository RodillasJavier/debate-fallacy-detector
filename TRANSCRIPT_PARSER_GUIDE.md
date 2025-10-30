# Debate Transcript Parser - Usage Guide

## Overview
The `parse_transcripts.py` script converts raw debate transcript text files into clean, normalized CSV format ready for analysis in your notebook.

## What it does
- **Parses**: All `.txt` files in `Debate Transcripts/` (1960-2020)
- **Extracts**: Speaker names, statements, dates, years
- **Normalizes**: Speaker names (e.g., "MR. NIXON" → "Richard Nixon")
- **Outputs**: 
  - `all_debates_combined.csv` — all debates in one file (8,139+ statements)
  - `parsed_debates/*.csv` — individual CSV per debate

## CSV Format
Each row contains:
- `speaker` — normalized speaker name (e.g., "Barack Obama", "Moderator")
- `text` — the statement/utterance
- `date` — debate date (YYYY-MM-DD format)
- `year` — debate year (integer)
- `debate_id` — unique identifier (e.g., "1960_October_13_1960")

## Quick Start

### 1. Run the parser
```bash
python3 parse_transcripts.py
```

### 2. Load in notebook
```python
import pandas as pd

# Load all debates
debates = pd.read_csv('all_debates_combined.csv')

# Quick exploration
print(f"Total statements: {len(debates)}")
print(f"Date range: {debates['year'].min()} - {debates['year'].max()}")
print(f"\nSpeaker distribution:\n{debates['speaker'].value_counts()}")

# Filter by year or speaker
debates_2020 = debates[debates['year'] == 2020]
trump_statements = debates[debates['speaker'] == 'Donald Trump']
```

## Features

### Speaker Normalization
The script handles many variations:
- Title prefixes: `MR. NIXON` → `Richard Nixon`
- All caps: `OBAMA` → `Barack Obama`
- Moderators: `WALLACE`, `LEHRER` → `Moderator`

### Robust Parsing
Works across different transcript formats:
- 1960s: Simple name-colon format
- 2000s-2020s: More complex moderator introductions
- Handles multiple speakers per debate
- Filters out very short/invalid utterances

### Error Handling
- Skips malformed text
- Reports warnings for files with no extracted statements
- Continues processing even if one file fails

## Adding New Transcripts

1. Add `.txt` file to appropriate year folder in `Debate Transcripts/`
2. Filename should be: `Month Day, Year.txt` (e.g., `October 15, 2024.txt`)
3. Format: Speaker names in ALL CAPS followed by colon
   ```
   MODERATOR: Welcome to the debate.
   CANDIDATE_A: Thank you for having me.
   CANDIDATE_B: Glad to be here.
   ```
4. Re-run: `python3 parse_transcripts.py`

## Customization

### Add New Speaker Mappings
Edit `normalize_speaker_name()` in `parse_transcripts.py`:

```python
name_mapping = {
    'KENNEDY': 'John F. Kennedy',
    'NEW_CANDIDATE': 'New Candidate Name',  # Add here
    # ...
}
```

### Change Output Location
Edit paths in `main()`:

```python
output_dir = script_dir / 'my_custom_output'  # Change this
```

## Troubleshooting

### No statements extracted?
- Check file encoding (should be UTF-8 or ASCII)
- Verify speaker names are in ALL CAPS followed by colon
- Look for the warning message in terminal output

### Speaker names wrong?
- Update `name_mapping` dictionary
- Re-run parser

### Missing debates?
- Check filename format: `Month Day, Year.txt`
- Ensure file is in a subdirectory of `Debate Transcripts/`

## Statistics

Current parsed data (as of last run):
- **43 debates** (1960-2020)
- **8,139+ statements** total
- Years covered: 1960, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020
