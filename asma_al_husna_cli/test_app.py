#!/usr/bin/env python3
"""Quick test of the Asma al-Husna CLI application"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from data_loader import DataLoader
from randomizer import UltraRandomizer


def test_data_loading():
    """Test that we can load the CSV files"""
    print("Testing data loading...")
    try:
        loader = DataLoader(Path(__file__).parent.parent)
        names = loader.load_all_names()
        print(f"✓ Successfully loaded {len(names)} names")
        
        # Show first few names
        print("\nFirst 5 names:")
        for name in names[:5]:
            print(f"  {name.number}. {name.name_arabic}")
            
        return True
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False


def test_randomizer():
    """Test the randomizer functionality"""
    print("\n\nTesting randomizer...")
    try:
        randomizer = UltraRandomizer()
        
        # Test entropy collection
        randomizer.collect_system_entropy()
        randomizer.add_user_entropy("Test intention for randomness")
        
        # Test shuffling
        test_items = list(range(1, 100))
        shuffled = randomizer.ultra_shuffle(test_items, "Test shuffle")
        
        print(f"✓ Randomizer working")
        print(f"  Original first 10: {test_items[:10]}")
        print(f"  Shuffled first 10: {shuffled[:10]}")
        
        # Show entropy report
        print("\n" + randomizer.get_entropy_report())
        
        return True
    except Exception as e:
        print(f"✗ Error in randomizer: {e}")
        return False


def test_selection():
    """Test the complete selection process"""
    print("\n\nTesting selection process...")
    try:
        # Load names
        loader = DataLoader(Path(__file__).parent.parent)
        names = loader.load_all_names()
        
        # Create randomizer and select
        randomizer = UltraRandomizer()
        selected = randomizer.select_one(names, "Test selection process")
        
        print(f"✓ Selected name: {selected.name_arabic}")
        print(f"  Number: {selected.number}")
        print(f"  Brief meaning: {selected.brief_meaning[:50]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error in selection: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Asma al-Husna CLI Test Suite")
    print("=" * 60)
    
    tests = [
        test_data_loading(),
        test_randomizer(),
        test_selection()
    ]
    
    print("\n" + "=" * 60)
    if all(tests):
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 60)