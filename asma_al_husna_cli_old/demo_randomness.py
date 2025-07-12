#!/usr/bin/env python3
"""
Demonstrate the ultra-randomness of the selection algorithm
by performing multiple selections and showing the distribution
"""

import sys
from pathlib import Path
from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.progress import track

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from data_loader import DataLoader
from randomizer import UltraRandomizer

console = Console()


def run_randomness_demo(iterations: int = 999):
    """Run multiple selections to demonstrate randomness distribution"""

    console.print("\n[bold gold]Ultra-Randomness Demonstration[/]\n")
    console.print(f"Running {iterations} selections to show distribution...\n")

    # Load names
    loader = DataLoader(Path(__file__).parent.parent)
    names = loader.load_all_names()

    # Track selections
    selections = Counter()
    randomizer = UltraRandomizer()

    # Run selections with progress bar
    for i in track(range(iterations), description="Selecting names..."):
        # Use different user input each time for more entropy
        user_input = f"Iteration {i} with unique entropy seed"
        selected = randomizer.select_one(names, user_input)
        selections[selected.number] += 1

    # Calculate statistics
    expected_freq = iterations / 99
    total_names_selected = len(selections)

    # Create results table
    table = Table(
        title="Selection Distribution Analysis",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    table.add_row("Total iterations", str(iterations))
    table.add_row("Unique names selected", f"{total_names_selected} / 99")
    table.add_row("Expected frequency per name", f"{expected_freq:.2f}")
    table.add_row("Coverage percentage", f"{(total_names_selected / 99) * 100:.1f}%")

    console.print("\n")
    console.print(table)

    # Show most and least selected
    most_common = selections.most_common(5)
    least_common = selections.most_common()[-5:]

    console.print("\n[bold purple]Most frequently selected:[/]")
    for num, count in most_common:
        name = next(n for n in names if n.number == num)
        deviation = ((count - expected_freq) / expected_freq) * 100
        console.print(
            f"  #{num}: {count} times ({deviation:+.1f}% from expected) - {name.name_arabic}"
        )

    console.print("\n[bold purple]Least frequently selected:[/]")
    for num, count in reversed(least_common):
        name = next(n for n in names if n.number == num)
        deviation = ((count - expected_freq) / expected_freq) * 100
        console.print(
            f"  #{num}: {count} times ({deviation:+.1f}% from expected) - {name.name_arabic}"
        )

    # Calculate chi-square statistic for randomness quality
    chi_square = sum(
        (count - expected_freq) ** 2 / expected_freq for count in selections.values()
    )
    chi_square += (
        99 - total_names_selected
    ) * expected_freq  # Account for unselected names

    console.print(f"\n[bold yellow]Chi-square statistic:[/] {chi_square:.2f}")
    console.print("[dim]Lower values indicate better randomness distribution[/]")

    # Show entropy report from last selection
    console.print("\n[bold cyan]Entropy Report (from last selection):[/]")
    console.print(randomizer.get_entropy_report())

    # Conclusion
    console.print("\n[bold gold]Conclusion:[/]")
    if total_names_selected >= 90:
        console.print("✓ Excellent distribution - high quality randomness achieved!")
    elif total_names_selected >= 80:
        console.print("✓ Good distribution - randomness is working well")
    else:
        console.print("⚠ Distribution could be improved - consider more iterations")


if __name__ == "__main__":
    import typer

    app = typer.Typer()

    @app.command()
    def demo(
        iterations: int = typer.Option(
            999, "--iterations", "-i", help="Number of selections to perform"
        )
    ):
        """Demonstrate the ultra-randomness of the selection algorithm"""
        run_randomness_demo(iterations)

    app()
