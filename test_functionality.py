#!/usr/bin/env python3
"""Automated functionality testing script for Aysekai International"""

import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(cmd, timeout=10):
    """Run command and capture output"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=Path(__file__).parent / "asma_al_husna_cli"
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"

def test_basic_commands():
    """Test all basic CLI commands"""
    tests = [
        ("python main.py about", 0),
        ("python main.py list-names --help", 0),
        ("python main.py meditate --help", 0),
    ]
    
    for cmd, expected_code in tests:
        code, stdout, stderr = run_command(cmd)
        if code != expected_code:
            print(f"❌ FAIL: {cmd} returned {code}, expected {expected_code}")
            print(f"   Error: {stderr}")
        else:
            print(f"✅ PASS: {cmd}")

def test_data_availability():
    """Check if required data files exist"""
    base = Path(__file__).parent
    required_files = [
        "data/processed/all_remaining_names_for_notion.csv",
        "data/processed/asma_al_husna_notion_ready.csv"
    ]
    
    for file in required_files:
        path = base / file
        if path.exists():
            print(f"✅ PASS: {file} exists")
        else:
            print(f"❌ FAIL: {file} missing")

def test_listing_commands():
    """Test list-names command variations"""
    tests = [
        "python main.py list-names",
        "python main.py list-names 1 10",
        "python main.py list-names 90 99",
    ]
    
    for cmd in tests:
        code, stdout, stderr = run_command(cmd, timeout=15)
        if code == 0 and stdout:
            print(f"✅ PASS: {cmd}")
        else:
            print(f"❌ FAIL: {cmd}")
            if stderr:
                print(f"   Error: {stderr}")

def test_meditation_flags():
    """Test meditation command with various flags"""
    # Using echo to provide input non-interactively
    tests = [
        'echo "test" | python main.py meditate',
        'echo "test" | python main.py meditate --baghdad',
        'echo "test" | python main.py meditate --entropy',
        'python main.py meditate --number 33',
    ]
    
    for cmd in tests:
        code, stdout, stderr = run_command(cmd, timeout=5)
        if code == 0:
            print(f"✅ PASS: {cmd}")
        else:
            print(f"❌ FAIL: {cmd}")
            if stderr and "error" in stderr.lower():
                print(f"   Error: {stderr}")

def test_concurrent_access():
    """Test multiple simultaneous instances"""
    import threading
    
    results = []
    
    def run_instance(instance_id):
        cmd = f"echo 'test{instance_id}' | python main.py meditate"
        code, _, stderr = run_command(cmd, timeout=5)
        results.append((instance_id, code == 0, stderr))
    
    threads = []
    for i in range(3):  # Reduced from 5 to be less aggressive
        t = threading.Thread(target=run_instance, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(0.1)  # Small delay between launches
    
    for t in threads:
        t.join()
    
    success_count = sum(1 for _, success, _ in results if success)
    if success_count == len(results):
        print(f"✅ PASS: All {len(results)} concurrent instances succeeded")
    else:
        print(f"❌ FAIL: Only {success_count}/{len(results)} concurrent instances succeeded")
        for instance_id, success, stderr in results:
            if not success and stderr:
                print(f"   Instance {instance_id} error: {stderr}")

def test_error_handling():
    """Test error scenarios"""
    tests = [
        ("python main.py meditate --number 0", 2),      # Invalid number
        ("python main.py meditate --number 100", 2),    # Invalid number
        ("python main.py unknown-command", 2),          # Unknown command
    ]
    
    for cmd, expected_code in tests:
        code, stdout, stderr = run_command(cmd, timeout=5)
        if code == expected_code:
            print(f"✅ PASS: {cmd} correctly failed with code {code}")
        else:
            print(f"❌ FAIL: {cmd} returned {code}, expected {expected_code}")

def test_dependencies():
    """Check if required dependencies are installed"""
    try:
        import typer
        import rich
        print("✅ PASS: Core dependencies (typer, rich) are installed")
    except ImportError as e:
        print(f"❌ FAIL: Missing core dependency: {e}")
    
    # Check optional dependencies
    optional_deps = [
        ("python-bidi", "Arabic text support"),
        ("pyfiglet", "ASCII art generation")
    ]
    
    for module, description in optional_deps:
        try:
            __import__(module.replace("-", "_"))
            print(f"✅ INFO: Optional dependency '{module}' ({description}) is installed")
        except ImportError:
            print(f"ℹ️  INFO: Optional dependency '{module}' ({description}) is not installed")

if __name__ == "__main__":
    print("=== Aysekai International Functionality Tests ===")
    print(f"Running from: {Path.cwd()}")
    print(f"Python version: {sys.version.split()[0]}")
    print("=" * 50 + "\n")
    
    print("1. Testing dependencies...")
    test_dependencies()
    
    print("\n2. Testing data availability...")
    test_data_availability()
    
    print("\n3. Testing basic commands...")
    test_basic_commands()
    
    print("\n4. Testing list-names variations...")
    test_listing_commands()
    
    print("\n5. Testing meditation flags...")
    test_meditation_flags()
    
    print("\n6. Testing error handling...")
    test_error_handling()
    
    print("\n7. Testing concurrent access...")
    test_concurrent_access()
    
    print("\n" + "=" * 50)
    print("=== Tests Complete ===")
    print("\nNote: Some tests may fail if:")
    print("- Dependencies are not installed")
    print("- CSV data files are missing")
    print("- Running from wrong directory")
    print("\nRun from project root with: python test_functionality.py")