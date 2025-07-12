"""Main CLI entry point with dependency injection"""

import typer
from typing import Optional, cast
from rich import print as rprint

from .error_handler import error_boundary, setup_exception_handler
from .dependencies import get_container
from ..di.interfaces import DataReader, RandomSelector, SessionLogger

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
    # Get dependencies from container
    container = get_container()
    data_reader = cast(DataReader, container.get(cast(type, DataReader)))
    random_selector = cast(RandomSelector, container.get(cast(type, RandomSelector)))
    session_logger = cast(SessionLogger, container.get(cast(type, SessionLogger)))
    
    # Load the divine names using injected data reader
    rprint("\n[dim]Loading the sacred names...[/]")
    
    try:
        names = data_reader.read_all_names()
        
        if not names:
            rprint("[red]No names could be loaded. Please check the data files.[/]")
            return
        
        rprint(f"[green]Loaded {len(names)} sacred names[/]")
        
        # Select name (specific or random)
        if name_number is not None:
            try:
                selected_name = data_reader.get_name_by_number(name_number)
            except ValueError:
                rprint(f"[red]Name #{name_number} not found. Please choose 1-99.[/]")
                return
        else:
            # Use random selector with default intention
            intention = "I seek divine guidance"
            selected_name = random_selector.select_random_name(names, intention)
            
            # Show entropy report if requested
            if show_entropy:
                entropy_report = random_selector.get_entropy_report()
                rprint(f"[dim]Entropy sources: {entropy_report.get('sources', [])}[/]")
        
        # Log the session
        session_logger.log_session(
            "direct selection" if name_number else "random selection",
            selected_name.number,
            selected_name.transliteration
        )
        
        # Display the selected name
        rprint(f"\n[bold blue]{selected_name.display_name}[/]")
        rprint(f"[italic]{selected_name.meaning_summary}[/]")
        
    except Exception as e:
        rprint(f"[red]Error during meditation: {str(e)}[/]")
        return


@app.command()
@error_boundary()
def list_names(
    start: Optional[int] = typer.Argument(None, help="Start number (1-99)"),
    end: Optional[int] = typer.Argument(None, help="End number (1-99)"),
):
    """List the 99 Beautiful Names of Allah"""
    # Get dependencies from container
    container = get_container()
    data_reader = cast(DataReader, container.get(cast(type, DataReader)))
    
    try:
        # Load names using injected data reader
        names = data_reader.read_all_names()
        
        if not names:
            rprint("[red]No names could be loaded.[/]")
            return
        
        # Filter by range if specified
        if start is not None and end is not None:
            names = [n for n in names if start <= n.number <= end]
        elif start is not None:
            names = [n for n in names if n.number >= start]
        
        # Display names
        for name in names:
            rprint(f"{name.number:2d}. [bold]{name.arabic}[/] ({name.transliteration}) - {name.brief_meaning}")
    
    except Exception as e:
        rprint(f"[red]Error listing names: {str(e)}[/]")
        return


@app.command()
def about():
    """Show information about this application"""
    rprint("[bold blue]Aysekai - Islamic Meditation CLI[/]")
    rprint("A mystical journey through the 99 Beautiful Names of Allah")
    rprint("Using modern Python architecture for spiritual practice")
    rprint("\n[dim]Version 2.0.0[/]")


if __name__ == "__main__":
    app()