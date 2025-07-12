#!/usr/bin/env python3
"""
Fix CSV formatting for Notion import
Addresses issues with multi-line content in Ta'wil column being truncated
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.aysekai.utils import constants, content, csv_handler, validators


def fix_csv_for_notion(input_file: Path, output_file: Path):
    """Fix CSV file for proper Notion import"""
    print(f"Reading from: {input_file}")
    print(f"Writing to: {output_file}")

    reader = csv_handler.AsmaCSVReader()
    writer = csv_handler.AsmaCSVWriter()
    validator = csv_handler.CSVValidator()

    fixed_rows = []
    total_rows = 0
    skipped_rows = 0

    try:
        # Read raw CSV data for row-by-row validation
        raw_data = reader.read_raw(input_file)

        # Process header separately
        if raw_data and "The Beautiful Name" in str(raw_data[0]):
            header_processed = False
        else:
            # Add default header if missing
            fixed_rows.append(
                {
                    "name": constants.COLUMN_HEADERS[0],
                    "number": constants.COLUMN_HEADERS[1],
                    "meaning": constants.COLUMN_HEADERS[2],
                    "tawil": constants.COLUMN_HEADERS[3],
                    "reference": constants.COLUMN_HEADERS[4],
                    "verse": constants.COLUMN_HEADERS[5],
                    "dhikr": constants.COLUMN_HEADERS[6],
                    "pronunciation": constants.COLUMN_HEADERS[7],
                    "phonetics": constants.COLUMN_HEADERS[8],
                }
            )
            header_processed = True

        # Process each row
        for row_num, row in enumerate(raw_data):
            total_rows += 1

            # Skip header if not yet processed
            if not header_processed and "The Beautiful Name" in str(row):
                header_processed = True
                continue

            # Validate row has correct number of columns
            if not validator.validate_columns(row):
                print(
                    f"Skipping malformed row {row_num + 1}: has {len(row)} columns instead of {constants.CSV_COLUMN_COUNT}"
                )
                skipped_rows += 1
                continue

            # Process the row
            processed_row = {
                "name": content.clean_multiline_content(row[0]),
                "number": row[1],
                "meaning": content.clean_multiline_content(row[2]),
                "tawil": content.process_tawil_sections(row[3]),
                "reference": content.clean_multiline_content(row[4]),
                "verse": content.clean_multiline_content(row[5]),
                "dhikr": content.format_dhikr_content(row[6]),
                "pronunciation": row[7],
                "phonetics": row[8],
            }

            # Validate content
            errors = validators.validate_name_data(processed_row)
            if errors:
                print(f"⚠️  Row {row_num + 1} has validation issues: {errors}")
                # Still include the row but warn about issues

            fixed_rows.append(processed_row)

    except Exception as e:
        print(f"Error processing CSV: {e}")
        raise

    # Write the fixed CSV
    writer.write_notion_format(fixed_rows, output_file)

    print(f"✅ Processed {total_rows} total rows")
    print(f"✅ Fixed {len(fixed_rows)} valid rows")
    print(f"✅ Filtered out {skipped_rows} malformed rows")
    print(f"✅ Fixed CSV saved to: {output_file}")

    # Show sample of Ta'wil content to verify
    if len(fixed_rows) > 1:
        print("\n📝 Sample Ta'wil content (row 2):")
        tawil_content = fixed_rows[1]["tawil"]
        print(f"Length: {len(tawil_content)} characters")
        print(f"Preview: {tawil_content[:200]}...")
        if any(emoji in tawil_content for emoji in ["📿", "🚶", "💎", "🌟"]):
            print("✅ Ta'wil sections properly formatted with emoji markers")


def main():
    """Main entry point"""
    # Use paths relative to script location
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    input_file = project_root / "names.csv"
    output_file = project_root / "data" / "processed" / "names_fixed_for_notion.csv"

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        fix_csv_for_notion(input_file, output_file)
        print(f"\n🎉 Success! Import {output_file.name} into Notion")
        print("📊 All content has been cleaned and formatted")
        print("💡 Multi-line content preserved with proper formatting")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
