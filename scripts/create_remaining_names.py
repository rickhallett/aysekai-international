#!/usr/bin/env python3
"""
Create CSV with the remaining Beautiful Names (excluding the ones already in Notion)
Extracts from the original names.csv and formats properly for Notion import
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from asma_core import constants, content, parser, csv_handler, validators


def extract_names_from_original(input_file: Path):
    """Extract all names from the original names.csv file"""
    print(f"Extracting names from {input_file}...")

    reader = csv_handler.AsmaCSVReader()
    names_data = []
    excluded_count = 0

    try:
        # Try standard CSV reading first
        all_names = reader.read_names(input_file)

        for name_dict in all_names:
            name = name_dict["name"]

            # Check if already in Notion
            if parser.is_existing_name(name):
                print(f"Excluding {name} (already in Notion)")
                excluded_count += 1
                continue

            names_data.append(name_dict)

    except Exception as e:
        print(f"Standard parsing failed: {e}")
        print("Attempting alternative parsing method...")

        # Fallback to line-by-line parsing
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            current_entry = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Check if this looks like a name entry
                name, _ = parser.extract_name_from_line(line)
                if name and parser.parse_name_with_arabic(name)[1]:  # Has Arabic
                    # Process previous entry if exists
                    if (
                        current_entry
                        and len(current_entry[0].split('","'))
                        >= constants.CSV_COLUMN_COUNT
                    ):
                        parsed_name = current_entry[0].split('","')[0].strip('"')
                        if not parser.is_existing_name(parsed_name):
                            names_data.append(parse_entry_to_dict(current_entry))

                    # Start new entry
                    current_entry = [line]
                elif current_entry:
                    current_entry.append(line)

            # Process last entry
            if current_entry:
                parsed_name = current_entry[0].split('","')[0].strip('"')
                if not parser.is_existing_name(parsed_name):
                    names_data.append(parse_entry_to_dict(current_entry))

        except Exception as e2:
            print(f"Alternative parsing also failed: {e2}")
            return []

    print(f"Extracted {len(names_data)} names")
    print(f"Excluded {excluded_count} names already in Notion")

    return names_data


def parse_entry_to_dict(entry_lines):
    """Parse entry lines into a dictionary"""
    import re

    # Join lines and parse
    full_text = " ".join(entry_lines)

    # Remove outer quotes
    if full_text.startswith('"') and full_text.endswith('"'):
        full_text = full_text[1:-1]

    # Split by '","'
    fields = re.split(r'",\s*"', full_text)

    # Ensure we have enough fields
    while len(fields) < constants.CSV_COLUMN_COUNT:
        fields.append("")

    return {
        "name": fields[0],
        "number": fields[1],
        "meaning": fields[2],
        "tawil": fields[3],
        "reference": fields[4],
        "verse": fields[5],
        "dhikr": fields[6],
        "pronunciation": fields[7],
        "phonetics": fields[8],
    }


def create_remaining_names_csv(input_file: Path, output_file: Path):
    """Create CSV with remaining names properly formatted for Notion"""
    print(f"Creating CSV with remaining names: {output_file}")

    # Extract names from original file
    names_data = extract_names_from_original(input_file)

    if not names_data:
        print("❌ Failed to extract names from CSV file")
        return 0

    # Process and clean data
    processed_data = []
    for name_dict in names_data:
        processed = {
            "name": content.clean_multiline_content(name_dict["name"]),
            "number": name_dict["number"],
            "meaning": content.clean_multiline_content(name_dict["meaning"]),
            "tawil": content.process_tawil_sections(name_dict["tawil"]),
            "reference": content.clean_multiline_content(name_dict["reference"]),
            "verse": content.clean_multiline_content(name_dict["verse"]),
            "dhikr": content.format_dhikr_content(name_dict["dhikr"]),
            "pronunciation": name_dict["pronunciation"],
            "phonetics": name_dict["phonetics"],
        }

        # Validate the processed data
        errors = validators.validate_name_data(processed)
        if errors:
            print(f"⚠️  Validation issues for {processed['name']}: {errors}")

        processed_data.append(processed)

    # Write to CSV
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
    output_file = project_root / "data" / "processed" / "remaining_names_for_notion.csv"

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        count = create_remaining_names_csv(input_file, output_file)
        if count > 0:
            print(
                f"\n🎉 Success! Import {output_file.name} into your existing Notion database"
            )
            print(f"📊 This file contains {count} Beautiful Names")
            print(
                f"✅ Excludes the {len(constants.EXISTING_NOTION_NAMES)} names already in your Notion database"
            )
            print(f"💡 All Ta'wil content preserved with proper formatting")
            print(f"🔄 Ready to merge with your existing Notion database")
        else:
            print("\n❌ Failed to extract names from the source file")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
