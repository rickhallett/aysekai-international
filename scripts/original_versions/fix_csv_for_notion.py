#!/usr/bin/env python3
"""
Fix CSV formatting for Notion import
Addresses issues with multi-line content in Ta'wil column being truncated
"""

import csv
import re


def clean_cell_content(content):
    """Clean and format cell content for proper CSV parsing"""
    if not content:
        return content

    # Convert actual line breaks to space + pipe + space for readability
    # This preserves the structure while keeping it in one cell
    content = re.sub(r"\n+", " | ", content)

    # Clean up multiple spaces
    content = re.sub(r"\s+", " ", content)

    # Clean up pipe spacing
    content = re.sub(r"\s*\|\s*", " | ", content)

    # Remove leading/trailing whitespace
    content = content.strip()

    # Handle problematic quote patterns
    content = re.sub(r'"{2,}', '"', content)

    return content


def fix_csv_for_notion(input_file, output_file):
    """Fix CSV file for proper Notion import"""
    print(f"Reading from: {input_file}")
    print(f"Writing to: {output_file}")

    fixed_rows = []
    total_rows = 0

    # Read and process the CSV
    with open(input_file, "r", encoding="utf-8") as file:
        # Use sniffer to detect CSV format
        sample = file.read(1024)
        file.seek(0)
        sniffer = csv.Sniffer()

        try:
            dialect = sniffer.sniff(sample, delimiters=",;")
        except:
            dialect = csv.excel

        reader = csv.reader(file, dialect=dialect)

        for row_num, row in enumerate(reader):
            total_rows += 1

            # Skip malformed rows (not exactly 9 columns)
            if len(row) != 9:
                print(
                    f"Skipping malformed row {row_num + 1}: has {len(row)} columns instead of 9"
                )
                continue

            # Clean each cell
            cleaned_row = []
            for i, cell in enumerate(row):
                cleaned_cell = clean_cell_content(cell)
                cleaned_row.append(cleaned_cell)

            fixed_rows.append(cleaned_row)

    # Write the fixed CSV
    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        for row in fixed_rows:
            writer.writerow(row)

    print(f"✅ Processed {total_rows} total rows")
    print(f"✅ Fixed {len(fixed_rows)} valid rows")
    print(f"✅ Filtered out {total_rows - len(fixed_rows)} malformed rows")
    print(f"✅ Fixed CSV saved to: {output_file}")

    # Show sample of Ta'wil content to verify
    if len(fixed_rows) > 1:
        print("\n📝 Sample Ta'wil content (row 2):")
        tawil_content = fixed_rows[1][3]  # Ta'wil is column 4 (index 3)
        print(f"Length: {len(tawil_content)} characters")
        print(f"Preview: {tawil_content[:200]}...")
        if "|" in tawil_content:
            print(f"✅ Multi-line content preserved with | separators")


if __name__ == "__main__":
    input_file = "names.csv"
    output_file = "names_fixed_for_notion.csv"

    try:
        fix_csv_for_notion(input_file, output_file)
        print(f"\n🎉 Success! Import {output_file} into Notion")
    except Exception as e:
        print(f"❌ Error: {e}")
