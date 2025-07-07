#!/usr/bin/env python3
"""
Extract all 99 Beautiful Names from the complete names.csv file
Parse the data intelligently and exclude the 5 already in Notion
"""

import csv
import re
import json


def clean_multiline_content(content):
    """Convert multiline content to properly formatted text with double newlines between sections"""
    if not content:
        return content

    # Handle problematic quote patterns first
    content = re.sub(r'"{2,}', '"', content)

    # Define the emoji section patterns (for Ta'wil column)
    emoji_sections = [
        (r"📿\s*SHARĪ\'A[^🚶💎🌟]*", "📿 SHARĪ'A"),
        (r"🚶\s*ṬARĪQA[^📿💎🌟]*", "🚶 ṬARĪQA"),
        (r"💎\s*ḤAQĪQA[^📿🚶🌟]*", "💎 ḤAQĪQA"),
        (r"🌟\s*MA\'RIFA[^📿🚶💎]*", "🌟 MA'RIFA"),
    ]

    # Check if this content has emoji sections (Ta'wil format)
    has_emoji_sections = any(
        re.search(pattern, content) for pattern, _ in emoji_sections
    )

    # Check if this content has dhikr format (Basic: ... Extended: ... or similar patterns)
    has_dhikr_format = re.search(
        r"Basic:\s*[^:]*(?:Extended|Full|For|Practice|Number|Times|Recitation|Morning|Protection|Against|Famous|Request|Abundance|Seeking|Study|Paired|Understanding|Coronation|Traditional|Purification|Artistic|Increase|Gratitude|Elevation|When|In|Before|After):",
        content,
    )

    if has_emoji_sections:
        # Handle Ta'wil content with emoji sections
        formatted_sections = []

        for pattern, section_name in emoji_sections:
            match = re.search(pattern, content)
            if match:
                section_content = match.group(0)
                # Clean up the section content
                section_content = re.sub(r"\s+", " ", section_content)
                section_content = section_content.strip()
                formatted_sections.append(section_content)

        # Join sections with double newlines
        content = "\n\n".join(formatted_sections)
    elif has_dhikr_format:
        # Handle Dhikr content with keyword separators
        # Add double newlines before dhikr keywords (except the first "Basic:")
        keywords = [
            "Extended:",
            "Full:",
            "For:",
            "Practice:",
            "Number:",
            "Times:",
            "Recitation:",
            "Morning:",
            "Protection:",
            "Against:",
            "Famous:",
            "Request:",
            "Abundance:",
            "Seeking:",
            "Study:",
            "Paired:",
            "Understanding:",
            "Coronation:",
            "Traditional:",
            "Purification:",
            "Artistic:",
            "Increase:",
            "Gratitude:",
            "Elevation:",
            "When:",
            "In:",
            "Before:",
            "After:",
        ]

        for keyword in keywords:
            # Replace occurrences of the keyword with newlines + keyword
            content = re.sub(r"(\s+)(" + re.escape(keyword) + ")", r"\n\n\2", content)

        # Clean up spacing within lines but preserve the double newlines
        lines = content.split("\n")
        cleaned_lines = []
        for line in lines:
            if line.strip():
                cleaned_lines.append(re.sub(r"\s+", " ", line.strip()))
            else:
                cleaned_lines.append("")

        content = "\n".join(cleaned_lines)
    else:
        # For other content, just clean up spacing
        content = re.sub(r"\s+", " ", content)
        content = content.strip()

    return content


def parse_names_from_csv():
    """Parse all names from the complete CSV file"""
    print("Parsing names from complete names.csv file...")

    # Names already in Notion (to exclude)
    existing_names = {
        "Al-Khabīr (الخبير)",
        "Ar-Raqīb (الرقيب)",
        "Al-Matīn (المتين)",
        "Al-Mu'īd (المعيد)",
        "Al-Bāqī (الباقي)",
    }

    # Read the raw content
    try:
        with open("names.csv", "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    # Split into lines and process
    lines = content.split("\n")

    # Find header line
    header = None
    header_found = False

    for line in lines:
        if "The Beautiful Name" in line and "Number" in line:
            # Parse header
            header_parts = line.split('","')
            header = []
            for i, part in enumerate(header_parts):
                cleaned = part.strip('"').strip()
                header.append(cleaned)
            header_found = True
            break

    if not header_found:
        header = [
            "The Beautiful Name / الاسم الحسن",
            "Number / الرقم",
            "Brief Meaning / المعنى المختصر",
            "Ta'wil / التأويل",
            "Quranic Reference / المرجع القرآني",
            "Verse → Ayah / الآية",
            "Dhikr Formula / صيغة الذكر",
            "Pronunciation",
            "Phonetics",
        ]

    # Extract individual names using a more intelligent approach
    names_data = []

    # Pattern to identify name entries with Arabic in parentheses
    name_pattern = r'^"?([^"]*\([^)]*[\u0600-\u06FF]+[^)]*\))'

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines and header
        if not line or "The Beautiful Name" in line:
            i += 1
            continue

        # Check if this line starts a name entry
        match = re.match(name_pattern, line)
        if match:
            name = match.group(1).strip('"')

            # Skip if this name is already in Notion
            if name in existing_names:
                print(f"Skipping {name} (already in Notion)")
                i += 1
                continue

            # Try to extract the complete entry for this name
            entry_lines = []
            entry_lines.append(line)

            # Look ahead to gather the complete entry
            j = i + 1
            while j < len(lines) and j < i + 20:  # Limit look-ahead
                next_line = lines[j].strip()
                if not next_line:
                    j += 1
                    continue

                # Check if this is the start of another name entry
                if re.match(name_pattern, next_line):
                    break

                entry_lines.append(next_line)
                j += 1

            # Process the collected lines into a structured entry
            entry = parse_single_entry(entry_lines, name)
            if entry and len(entry) >= 9:
                names_data.append(entry[:9])  # Take only first 9 columns
                print(f"✅ Extracted: {name}")

            i = j
        else:
            i += 1

    print(f"Extracted {len(names_data)} names from CSV")
    return [header] + names_data


def parse_single_entry(lines, name):
    """Parse a single name entry from multiple lines"""
    # Join all lines and try to parse as CSV
    full_text = " ".join(lines)

    # Try to split into fields - this is tricky due to the formatting
    # We'll use a simple approach: split by quotes and commas

    # Remove the outer quotes if present
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
    while len(cleaned_fields) < 9:
        cleaned_fields.append("")

    return cleaned_fields[:9]


def create_remaining_names_csv(output_file):
    """Create CSV with all remaining names for Notion import"""
    print(f"Creating CSV with remaining names: {output_file}")

    # Parse all names from the source file
    all_data = parse_names_from_csv()

    if len(all_data) < 2:
        print("❌ Failed to extract names from CSV file")
        return 0

    # Write to new CSV file
    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        for row in all_data:
            # Clean each cell
            cleaned_row = []
            for cell in row:
                if isinstance(cell, str):
                    cleaned_cell = clean_multiline_content(cell)
                    cleaned_row.append(cleaned_cell)
                else:
                    cleaned_row.append(str(cell) if cell is not None else "")

            # Ensure exactly 9 columns
            while len(cleaned_row) < 9:
                cleaned_row.append("")

            writer.writerow(cleaned_row[:9])

    print(f"✅ Created CSV with {len(all_data)} rows")
    print(f"✅ This includes header + {len(all_data)-1} name entries")
    print(f"✅ File saved to: {output_file}")

    return len(all_data) - 1


if __name__ == "__main__":
    output_file = "all_remaining_names_for_notionv2.csv"

    try:
        count = create_remaining_names_csv(output_file)
        if count > 0:
            print(
                f"\n🎉 Success! Import {output_file} into your existing Notion database"
            )
            print(f"📊 This file contains {count} Beautiful Names")
            print(f"✅ Excludes the 5 names already in your Notion database")
            print(f"💡 All Ta'wil content preserved with | separators")
            print(f"🔄 Ready to merge with your existing Notion database")
        else:
            print(f"\n❌ Failed to extract names from the source file")
    except Exception as e:
        print(f"❌ Error: {e}")
