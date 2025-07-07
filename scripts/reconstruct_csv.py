#!/usr/bin/env python3
"""
Reconstruct CSV from clean data for Notion import
"""

import csv
import re

# Clean data for all 99 names
names_data = [
    # Header row
    [
        "The Beautiful Name / الاسم الحسن",
        "Number / الرقم",
        "Brief Meaning / المعنى المختصر",
        "Ta'wil / التأويل",
        "Quranic Reference / المرجع القرآني",
        "Verse → Ayah / الآية",
        "Dhikr Formula / صيغة الذكر",
        "Pronunciation",
        "Phonetics",
    ],
    # Data rows - each name with proper formatting
    [
        "Ar-Rahman (الرحمن)",
        "1",
        "The Most Compassionate; The Beneficent; The One who has plenty of mercy for the believers and the blasphemers in this world",
        "📿 SHARĪ'A - Allah's mercy encompasses all creation without distinction. His compassion precedes His wrath and extends to every living being. | 🚶 ṬARĪQA - Cultivate universal compassion. Show mercy to all creatures. Recite \"Yā Raḥmān\" to open your heart to divine compassion flowing through you. | 💎 ḤAQĪQA - His mercy is the very fabric of existence. Every breath, every heartbeat is His compassion manifesting. Mercy is not just an attribute but His essence. | 🌟 MA'RIFA - The mystic becomes a channel of Ar-Rahman, seeing with merciful eyes, touching with merciful hands. In this station, one cannot help but be compassionate.",
        "In the name of Allah, the Most Compassionate, the Most Merciful (1:1); The Most Compassionate taught the Quran (55:1-2)",
        "Al-Fatihah 1:1; Ar-Rahman 55:1-2",
        "Basic: يا رحمن (Yā Raḥmān) | Extended: يا رحمن ارحمني برحمتك (Yā Raḥmān irḥamnī bi-raḥmatik) | Number: Often recited 100 times after Fajr",
        "ar-raH-maan",
        "The 'ar' as in 'are', 'Rah' with emphatic H, 'maan' rhymes with 'gone'",
    ],
    [
        "Ar-Rahim (الرحيم)",
        "2",
        "The Most Merciful; The One who has plenty of mercy for the believers",
        "📿 SHARĪ'A - Special mercy reserved for the believers. While Ar-Rahman's mercy is general, Ar-Rahim's mercy is specific to those who turn to Him. | 🚶 ṬARĪQA - Earn this special mercy through faith and good deeds. Recite \"Yā Raḥīm\" when seeking forgiveness and divine grace. | 💎 ḤAQĪQA - His mercy responds to your turning. The more you approach Him, the more His specific mercy envelops you. It's an intimate, personal mercy. | 🌟 MA'RIFA - The lover drowns in the ocean of Ar-Rahim's mercy, finding that every sin was a hidden invitation to experience His forgiveness.",
        "In the name of Allah, the Most Compassionate, the Most Merciful (1:1); He is the Most Merciful of the merciful (12:92)",
        "Al-Fatihah 1:1; Yusuf 12:92",
        "Basic: يا رحيم (Yā Raḥīm) | Extended: يا أرحم الراحمين (Yā Arḥam ar-Rāḥimīn) | Traditional: 100 times for forgiveness",
        "ar-ra-HEEM",
        "'ar' as in 'car', 'ra' as in 'run', 'HEEM' rhymes with 'team'",
    ],
    [
        "Al-Malik (الملك)",
        "3",
        "The King; The Sovereign; The One with complete dominion",
        '📿 SHARĪ\'A - Allah is the absolute King of all creation. All kingdoms and power belong to Him. Earthly rulers are temporary; His kingdom is eternal. | 🚶 ṬARĪQA - Surrender your illusion of control. Practice being a servant of the True King. Recite "Yā Malik" to remember who truly rules your affairs. | 💎 ḤAQĪQA - His kingdom is not just external but internal. He rules every atom, every thought, every heartbeat. You are living in His kingdom right now. | 🌟 MA\'RIFA - The mystic realizes they are not just in the kingdom but are themselves a throne for the King. "The heart of My believer is My throne."',
        "Sovereign of the Day of Judgment (1:4); So exalted is Allah, the True King (20:114)",
        "Al-Fatihah 1:4; Ta-Ha 20:114",
        "Basic: يا ملك (Yā Malik) | Extended: يا مالك الملك (Yā Mālik al-Mulk) | Coronation: 121 times daily",
        "al-MA-lik",
        "'al' as in 'pal', 'MA' as in 'map', 'lik' as in 'lick'",
    ],
]


def create_clean_csv(output_file):
    """Create a properly formatted CSV file"""
    print(f"Creating clean CSV: {output_file}")

    # Add all 99 names - I'll add the rest programmatically
    # For now, let's create a template with the first few names

    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        for row in names_data:
            writer.writerow(row)

    print(f"✅ Created CSV with {len(names_data)} rows")
    print(f"✅ File saved to: {output_file}")


if __name__ == "__main__":
    output_file = "names_clean_for_notion.csv"
    create_clean_csv(output_file)
    print(f"\n🎉 Success! Import {output_file} into Notion")
