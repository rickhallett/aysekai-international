"""Main CLI entry point - updated with new package structure"""

import typer
from typing import Optional
from rich import print as rprint

from .path_resolver import get_path_resolver
from .error_handler import error_boundary, setup_exception_handler
from ..utils.csv_handler import AsmaCSVReader

# Setup global exception handler
setup_exception_handler()

app = typer.Typer(
    name="aysekai",
    help="Interactive CLI for daily meditation on the 99 Beautiful Names of Allah",
    add_completion=False,
)


@app.command()
@error_boundary()
def meditate(
    show_baghdad: bool = typer.Option(
        False, "--baghdad", "-b", help="Show Baghdad art instead of mosque"
    ),
    show_entropy: bool = typer.Option(
        False, "--entropy", "-e", help="Show entropy report for randomness transparency"
    ),
    name_number: Optional[int] = typer.Option(
        None,
        "--number",
        "-n",
        min=1,
        max=99,
        help="Select specific name by number (1-99)",
    ),
):
    """Begin your daily meditation journey through the 99 Beautiful Names"""
    # Get path resolver for CSV file access
    path_resolver = get_path_resolver()
    
    # Load the divine names using new CSV handler
    rprint("\n[dim]Loading the sacred names...[/]")
    
    # Find the first available CSV file
    csv_files = path_resolver.list_available_csvs()
    if not csv_files:
        rprint("[red]No CSV data files found. Please ensure data files are installed.[/]")
        return
    
    reader = AsmaCSVReader(csv_files[0])
    names = reader.read_all()
    
    if not names:
        rprint("[red]No names could be loaded. Please check the data files.[/]")
        return
    
    rprint(f"[green]Loaded {len(names)} sacred names[/]")
    
    # For now, just show the first name as a test
    if names:
        name = names[0] if name_number is None else next((n for n in names if n.number == name_number), names[0])
        rprint(f"\n[bold blue]{name.display_name}[/]")
        rprint(f"[italic]{name.meaning_summary}[/]")


@app.command()
@error_boundary()
def list_names(
    start: Optional[int] = typer.Argument(None, help="Start number (1-99)"),
    end: Optional[int] = typer.Argument(None, help="End number (1-99)"),
):
    """List the 99 Beautiful Names of Allah"""
    # Get data path and load names
    path_resolver = get_path_resolver()
    csv_files = path_resolver.list_available_csvs()
    
    if not csv_files:
        rprint("[red]No CSV data files found.[/]")
        return
    
    reader = AsmaCSVReader(csv_files[0])
    names = reader.read_all()
    
    # Filter by range if specified
    if start is not None and end is not None:
        names = [n for n in names if start <= n.number <= end]
    elif start is not None:
        names = [n for n in names if n.number >= start]
    
    # Display names
    for name in names:
        rprint(f"{name.number:2d}. [bold]{name.arabic}[/] ({name.transliteration}) - {name.brief_meaning}")


@app.command()
def about():
    """Show information about this application"""
    rprint("[bold blue]Aysekai - Islamic Meditation CLI[/]")
    rprint("A mystical journey through the 99 Beautiful Names of Allah")
    rprint("Using modern Python architecture for spiritual practice")
    rprint("\n[dim]Version 2.0.0[/]")


if __name__ == "__main__":
    app()