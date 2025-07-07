#!/usr/bin/env python3
"""
Asma al-Husna Interactive CLI
A mystical journey through the 99 Beautiful Names of Allah
Using ultra-random selection for daily meditation
"""

import typer
from typing import Optional
from pathlib import Path
import sys
from rich import print as rprint

# Add parent directory to path for CSV file access
sys.path.append(str(Path(__file__).parent.parent))

from data_loader import DataLoader, DivineName
from randomizer import UltraRandomizer
from ui import (
    print_intro, 
    prompt_user_intention, 
    show_processing_animation,
    display_divine_name,
    show_error,
    show_entropy_report,
    console
)
from ascii_art import get_intro_art, get_baghdad_art, get_divider


app = typer.Typer(
    name="asma-al-husna",
    help="Interactive CLI for daily meditation on the 99 Beautiful Names of Allah",
    add_completion=False
)


def get_data_files_path() -> Path:
    """Get the path to the CSV data files"""
    # Try multiple possible locations
    possible_paths = [
        Path(__file__).parent.parent,  # Parent directory
        Path.cwd(),  # Current directory
        Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "Documents" / "Manual Library" / "code" / "aysekai-international"
    ]
    
    for path in possible_paths:
        # Check new structure first
        csv1 = path / "data" / "processed" / "all_remaining_names_for_notion.csv"
        csv2 = path / "data" / "processed" / "asma_al_husna_notion_ready.csv"
        if csv1.exists() or csv2.exists():
            return path
            
    raise FileNotFoundError("Could not find the CSV data files. Please ensure they are in the correct location.")


@app.command()
def meditate(
    show_baghdad: bool = typer.Option(False, "--baghdad", "-b", help="Show Baghdad art instead of mosque"),
    show_entropy: bool = typer.Option(False, "--entropy", "-e", help="Show entropy report for randomness transparency"),
    name_number: Optional[int] = typer.Option(None, "--number", "-n", min=1, max=99, help="Select specific name by number (1-99)")
):
    """
    Begin your daily meditation journey through the 99 Beautiful Names
    """
    try:
        # Display introduction art
        if show_baghdad:
            print_intro(get_baghdad_art())
        else:
            print_intro(get_intro_art())
        
        # Load the divine names
        console.print(f"\n[dim]Loading the sacred names...[/]\n")
        data_path = get_data_files_path()
        loader = DataLoader(data_path)
        names = loader.load_all_names()
        
        if not names:
            show_error("Could not load the divine names. Please check the CSV files.")
            raise typer.Exit(1)
        
        console.print(f"[green]✓ Successfully loaded {len(names)} Beautiful Names[/]\n")
        
        # Handle specific name request
        if name_number:
            try:
                selected_name = loader.get_name_by_number(name_number)
                console.print(f"[purple]You have chosen name #{name_number}[/]\n")
            except ValueError:
                show_error(f"Name #{name_number} not found. Please choose a number between 1 and 99.")
                raise typer.Exit(1)
        else:
            # Get user intention
            intention = prompt_user_intention()
            
            if not intention.strip():
                intention = "I seek divine guidance"
            
            # Show processing animation
            show_processing_animation()
            
            # Perform ultra-random selection
            randomizer = UltraRandomizer()
            selected_name = randomizer.select_one(names, intention)
            
            # Show entropy report if requested
            if show_entropy:
                show_entropy_report(randomizer.get_entropy_report())
        
        # Display the selected name
        console.print(get_divider("arabic"))
        console.print()
        display_divine_name(selected_name)
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Journey interrupted. May peace be with you.[/]")
        raise typer.Exit(0)
    except Exception as e:
        show_error(f"An unexpected error occurred: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list_names(
    start: int = typer.Option(1, "--start", "-s", min=1, max=99, help="Starting number"),
    end: int = typer.Option(99, "--end", "-e", min=1, max=99, help="Ending number")
):
    """
    List all or a range of the 99 Beautiful Names
    """
    try:
        # Load names
        data_path = get_data_files_path()
        loader = DataLoader(data_path)
        names = loader.load_all_names()
        
        # Filter range
        filtered_names = [n for n in names if start <= n.number <= end]
        filtered_names.sort(key=lambda x: x.number)
        
        # Display header
        console.print(get_divider("ornate"))
        console.print(f"\n[bold gold]The Beautiful Names ({start}-{end})[/]\n")
        console.print(get_divider("simple"))
        
        # Display each name
        for name in filtered_names:
            # Extract just the name part without parentheses
            name_parts = name.name_arabic.split('(')
            arabic_name = name_parts[0].strip()
            
            console.print(f"[purple]{name.number:2d}[/]. [gold]{arabic_name}[/] - [italic]{name.brief_meaning[:60]}...[/]")
        
        console.print()
        console.print(get_divider("ornate"))
        
    except Exception as e:
        show_error(f"Error listing names: {str(e)}")
        raise typer.Exit(1)


@app.command()
def about():
    """
    About this application
    """
    about_text = """
    [bold gold]Asma al-Husna Interactive CLI[/]
    
    This application provides a mystical journey through the 99 Beautiful Names
    of Allah (الأسماء الحسنى), using cutting-edge randomness algorithms to select
    a name for daily meditation based on your personal intention.
    
    [purple]Features:[/]
    • Ultra-random selection using multiple entropy sources
    • Beautiful terminal UI with Arabic text support
    • Four levels of mystical interpretation (Ta'wīl)
    • Quranic references and dhikr formulas
    • Pronunciation guides for proper recitation
    
    [green]Randomness:[/]
    The selection process combines:
    - Cryptographically secure random generation
    - Nanosecond-precision timing
    - Your personal intention (SHA-256 hashed)
    - System entropy sources
    - Hardware random generation
    
    All mixed using XOR operations and Fisher-Yates shuffling
    for the closest approximation to true randomness possible
    on consumer hardware.
    
    [gold]May your journey be illuminated.[/]
    """
    
    console.print(get_divider("stars"))
    console.print(about_text)
    console.print(get_divider("stars"))


def main():
    """Entry point for the application"""
    app()


if __name__ == "__main__":
    main()