#!/usr/bin/env python3
"""
Extract all 99 Beautiful Names from the complete names.csv file
Parse the data intelligently and exclude the 5 already in Notion
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from asma_core import constants, content, parser, csv_handler, validators


def parse_names_from_csv(input_file: Path):
    """Parse all names from the complete CSV file"""
    print(f"Parsing names from {input_file}...")
    
    reader = csv_handler.AsmaCSVReader()
    
    try:
        # Read raw data first to handle special parsing
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    # Split into lines for special parsing
    lines = raw_content.split('\n')
    
    # Extract names using more intelligent approach
    names_data = []
    excluded_count = 0
    
    # Pattern to identify name entries
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and header
        if not line or "The Beautiful Name" in line:
            i += 1
            continue
        
        # Try to extract name from line
        name, number = parser.extract_name_from_line(line)
        
        if name and parser.parse_name_with_arabic(name)[1]:  # Has Arabic
            # Check if already in Notion
            if parser.is_existing_name(name):
                print(f"Skipping {name} (already in Notion)")
                excluded_count += 1
                i += 1
                continue
            
            # Collect entry lines
            entry_lines = [line]
            
            # Look ahead to gather complete entry
            j = i + 1
            while j < len(lines) and j < i + 20:
                next_line = lines[j].strip()
                if not next_line:
                    j += 1
                    continue
                
                # Check if this is start of another name
                next_name, _ = parser.extract_name_from_line(next_line)
                if next_name and parser.parse_name_with_arabic(next_name)[1]:
                    break
                
                entry_lines.append(next_line)
                j += 1
            
            # Parse the entry
            entry = parse_single_entry(entry_lines, name)
            if entry and validators.validate_row_length(entry):
                names_data.append(entry)
                print(f"✅ Extracted: {name}")
            
            i = j
        else:
            i += 1
    
    print(f"Extracted {len(names_data)} names from CSV")
    print(f"Excluded {excluded_count} names already in Notion")
    
    return names_data


def parse_single_entry(lines, name):
    """Parse a single name entry from multiple lines"""
    import re
    
    # Join all lines
    full_text = ' '.join(lines)
    
    # Remove outer quotes if present
    if full_text.startswith('"') and full_text.endswith('"'):
        full_text = full_text[1:-1]
    
    # Split by '","' pattern
    fields = re.split(r'",\s*"', full_text)
    
    # Clean up each field
    cleaned_fields = []
    for field in fields:
        cleaned = field.strip('"').strip()
        cleaned_fields.append(cleaned)
    
    # Ensure we have the right number of fields
    while len(cleaned_fields) < constants.CSV_COLUMN_COUNT:
        cleaned_fields.append("")
    
    return cleaned_fields[:constants.CSV_COLUMN_COUNT]


def create_remaining_names_csv(input_file: Path, output_file: Path):
    """Create CSV with all remaining names for Notion import"""
    print(f"Creating CSV with remaining names: {output_file}")
    
    # Parse all names from source file
    names_data = parse_names_from_csv(input_file)
    
    if not names_data:
        print("❌ Failed to extract names from CSV file")
        return 0
    
    # Prepare data for writing
    processed_data = []
    for row in names_data:
        processed_row = {
            'name': content.clean_multiline_content(row[0]),
            'number': row[1],
            'meaning': content.clean_multiline_content(row[2]),
            'tawil': content.process_tawil_sections(row[3]),
            'reference': content.clean_multiline_content(row[4]),
            'verse': content.clean_multiline_content(row[5]),
            'dhikr': content.format_dhikr_content(row[6]),
            'pronunciation': row[7],
            'phonetics': row[8]
        }
        processed_data.append(processed_row)
    
    # Write to CSV using our writer
    writer = csv_handler.AsmaCSVWriter()
    writer.write_notion_format(processed_data, output_file)
    
    print(f"✅ Created CSV with {len(processed_data)} name entries")
    print(f"✅ File saved to: {output_file}")
    
    return len(processed_data)


def main():
    """Main entry point"""
    # Use paths relative to script location
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    input_file = project_root / "names.csv"
    output_file = project_root / "data" / "processed" / "all_remaining_names_for_notion.csv"
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        count = create_remaining_names_csv(input_file, output_file)
        if count > 0:
            print(f"\n🎉 Success! Import {output_file.name} into your existing Notion database")
            print(f"📊 This file contains {count} Beautiful Names")
            print(f"✅ Excludes the {len(constants.EXISTING_NOTION_NAMES)} names already in your Notion database")
            print(f"💡 All Ta'wil content preserved with proper formatting")
            print(f"🔄 Ready to merge with your existing Notion database")
        else:
            print("\n❌ Failed to extract names from the source file")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()