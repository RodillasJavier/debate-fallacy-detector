#!/usr/bin/env python3

"""
Parse presidential debate transcripts into normalized CSV format.

This script processes debate transcripts from various years (1960-2020) which have
different formatting styles, and outputs clean CSV files with columns:
- speaker: normalized speaker name
- text: the statement/utterance
- date: debate date
- year: debate year
- debate_id: unique identifier

Usage:
    python parse_transcripts.py

Output:
    Creates 'parsed_debates/' directory with individual CSV files
    and 'all_debates_combined.csv' with all debates merged.
"""

import os
import re
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional


def extract_date_from_filename(filename: str) -> Tuple[str, int]:
    """
    Extract date and year from filename like 'September 26, 1960.txt'
    
    Returns:
        Tuple of (formatted_date, year)
    """
    # Remove .txt extension
    name = filename.replace('.txt', '')
    
    # Try to parse date
    try:
        date_obj = datetime.strptime(name, "%B %d, %Y")
        return date_obj.strftime("%Y-%m-%d"), date_obj.year
    except ValueError:
        # Fallback: extract year from parent directory
        year_match = re.search(r'(\d{4})', name)
        if year_match:
            year = int(year_match.group(1))
            return name, year
        return name, 0


def normalize_speaker_name(speaker: str) -> str:
    """
    Normalize speaker names for consistency.
    
    Examples:
        'MR. NIXON' -> 'Richard Nixon'
        'OBAMA' -> 'Barack Obama'
        'MODERATOR' -> 'Moderator'
    """
    speaker = speaker.strip().upper()
    
    # Remove common prefixes
    speaker = re.sub(r'^(MR\.|MS\.|MRS\.|DR\.|SENATOR|GOVERNOR|PRESIDENT|VICE PRESIDENT)\s+', '', speaker)
    
    # Moderator patterns
    if any(mod in speaker for mod in ['MODERATOR', 'LEHRER', 'WALLACE', 'SMITH']):
        return 'Moderator'
    
    # Known candidates mapping (add more as needed)
    name_mapping = {
        'KENNEDY': 'John F. Kennedy',
        'NIXON': 'Richard Nixon',
        'FORD': 'Gerald Ford',
        'CARTER': 'Jimmy Carter',
        'REAGAN': 'Ronald Reagan',
        'MONDALE': 'Walter Mondale',
        'BUSH': 'George H.W. Bush',
        'DUKAKIS': 'Michael Dukakis',
        'CLINTON': 'Bill Clinton',
        'DOLE': 'Bob Dole',
        'GORE': 'Al Gore',
        'GEORGE W. BUSH': 'George W. Bush',
        'KERRY': 'John Kerry',
        'OBAMA': 'Barack Obama',
        'MCCAIN': 'John McCain',
        'ROMNEY': 'Mitt Romney',
        'TRUMP': 'Donald Trump',
        'BIDEN': 'Joe Biden',
    }
    
    # Check mapping
    for key, value in name_mapping.items():
        if key in speaker:
            return value
    
    # If no match, return title-cased version
    return speaker.title()


def parse_transcript(file_path: str) -> List[Dict[str, str]]:
    """
    Parse a single debate transcript file.
    
    Returns:
        List of dictionaries with keys: speaker, text, date, year, debate_id
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract metadata
    filename = os.path.basename(file_path)
    date_str, year = extract_date_from_filename(filename)
    debate_id = f"{year}_{filename.replace('.txt', '').replace(' ', '_').replace(',', '')}"
    
    statements = []
    
    # Pattern 1: Speaker name in ALL CAPS followed by colon
    # Matches: "KENNEDY:", "MR. NIXON:", "MODERATOR:", etc.
    pattern = r'^([A-Z][A-Z\s\.,]+?):\s*(.+?)(?=^[A-Z][A-Z\s\.,]+?:|$)'
    
    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        speaker_raw = match.group(1).strip()
        text = match.group(2).strip()
        
        # Skip very short utterances (likely errors)
        if len(text) < 10:
            continue
        
        # Normalize speaker
        speaker = normalize_speaker_name(speaker_raw)
        
        # Clean text: remove excessive whitespace, newlines
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        if text:
            statements.append({
                'speaker': speaker,
                'text': text,
                'date': date_str,
                'year': year,
                'debate_id': debate_id
            })
    
    return statements


def parse_all_transcripts(transcripts_dir: str, output_dir: str) -> None:
    """
    Parse all transcript files and save as individual CSVs plus a combined CSV.
    
    Args:
        transcripts_dir: Path to 'Debate Transcripts' folder
        output_dir: Path to output directory for parsed CSVs
    """
    transcripts_path = Path(transcripts_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    all_statements = []
    processed_count = 0
    
    # Find all .txt files recursively
    txt_files = list(transcripts_path.rglob('*.txt'))
    
    print(f"Found {len(txt_files)} transcript files.")
    print("Parsing transcripts...")
    
    for txt_file in sorted(txt_files):
        print(f"  Processing: {txt_file.name}")
        
        try:
            statements = parse_transcript(str(txt_file))
            
            if not statements:
                print(f"    ⚠️  Warning: No statements extracted from {txt_file.name}")
                continue
            
            # Save individual CSV
            output_csv = output_path / f"{statements[0]['debate_id']}.csv"
            save_to_csv(statements, output_csv)
            
            all_statements.extend(statements)
            processed_count += 1
            print(f"    ✓ Extracted {len(statements)} statements")
            
        except Exception as e:
            print(f"    ✗ Error processing {txt_file.name}: {e}")
    
    # Save combined CSV
    if all_statements:
        combined_csv = output_path.parent / 'all_debates_combined.csv'
        save_to_csv(all_statements, combined_csv)
        print(f"\n✓ Successfully processed {processed_count} debates")
        print(f"✓ Total statements extracted: {len(all_statements)}")
        print(f"✓ Combined CSV saved to: {combined_csv}")
        print(f"✓ Individual CSVs saved to: {output_path}/")
    else:
        print("\n✗ No statements extracted from any transcripts.")


def save_to_csv(statements: List[Dict[str, str]], output_file: Path) -> None:
    """Save statements to CSV file."""
    if not statements:
        return
    
    fieldnames = ['speaker', 'text', 'date', 'year', 'debate_id']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(statements)


def main():
    """Main entry point."""
    # Paths relative to script location
    script_dir = Path(__file__).parent
    transcripts_dir = script_dir / 'Debate Transcripts'
    output_dir = script_dir / 'parsed_debates'
    
    if not transcripts_dir.exists():
        print(f"Error: Transcripts directory not found at {transcripts_dir}")
        print("Please ensure 'Debate Transcripts/' folder exists in the same directory as this script.")
        return
    
    print("=" * 60)
    print("Presidential Debate Transcript Parser")
    print("=" * 60)
    
    parse_all_transcripts(str(transcripts_dir), str(output_dir))
    
    print("\n" + "=" * 60)
    print("Parsing complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check the 'parsed_debates/' folder for individual CSV files")
    print("2. Use 'all_debates_combined.csv' in your notebook")
    print("3. Load with: pd.read_csv('all_debates_combined.csv')")


if __name__ == '__main__':
    main()
