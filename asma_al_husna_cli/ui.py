"""Rich UI components for beautiful terminal display"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt
from rich.table import Table
from rich.layout import Layout
from rich.style import Style
from rich.box import ROUNDED, DOUBLE, ASCII
from rich import print as rprint
import time
from typing import Optional
from data_loader import DivineName


# Color scheme
COLORS = {
    "purple": "#9D4EDD",      # Royal Purple
    "gold": "#FFD700",        # Gold
    "green": "#10B981",       # Emerald Green
    "light_purple": "#C77DFF",
    "dark_purple": "#7209B7",
    "white": "#FFFFFF",
    "arabic": "#FFD700",      # Gold for Arabic text
    "meaning": "#E9C46A",     # Soft gold for meanings
    "reference": "#10B981",   # Green for Quranic references
}

console = Console()


def print_intro(art: str) -> None:
    """Display introduction art with styling"""
    intro_text = Text(art)
    intro_text.stylize(f"bold {COLORS['gold']}")
    console.print(Align.center(intro_text))


def prompt_user_intention() -> str:
    """Prompt user for their intention with beautiful styling"""
    console.print("\n")
    
    # Create prompt panel
    prompt_text = Text("Speak your truth for today...\n", style=f"bold {COLORS['purple']}")
    prompt_text.append("Share your intention, your experience, your heart's whisper", style=f"italic {COLORS['light_purple']}")
    
    panel = Panel(
        Align.center(prompt_text),
        title="[bold gold]✦ Your Sacred Intention ✦[/]",
        title_align="center",
        border_style=COLORS['gold'],
        box=ROUNDED,
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()
    
    # Get user input with styled prompt
    intention = Prompt.ask(
        f"[{COLORS['purple']}]►[/] [italic]Enter your intention[/]",
        console=console
    )
    
    return intention


def show_processing_animation(duration: float = 3.0) -> None:
    """Display mystical processing animation"""
    console.print("\n")
    
    messages = [
        "Gathering cosmic entropy...",
        "Mixing divine randomness...",
        "Consulting the celestial spheres...",
        "Weaving your intention into fate...",
        "Selecting your divine message..."
    ]
    
    with Progress(
        SpinnerColumn(spinner_name="dots12", style=COLORS['purple']),
        TextColumn("[bold purple]{task.description}[/]"),
        BarColumn(bar_width=40, style=COLORS['purple'], complete_style=COLORS['gold']),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Processing", total=len(messages))
        
        for message in messages:
            progress.update(task, description=message)
            progress.advance(task)
            time.sleep(duration / len(messages))
    
    console.print(f"\n[bold {COLORS['gold']}]✨ The veils have been lifted... ✨[/]\n")
    time.sleep(0.5)


def display_divine_name(name: DivineName) -> None:
    """Display the selected divine name in a beautiful format"""
    # Create main layout
    layout = Layout()
    
    # Title Section
    title_text = Text()
    title_text.append(f"{name.name_arabic}\n", style=f"bold {COLORS['arabic']} on black size=24")
    title_text.append(f"The {name.number}th Beautiful Name of Allah", style=f"italic {COLORS['light_purple']}")
    
    title_panel = Panel(
        Align.center(title_text),
        box=DOUBLE,
        border_style=COLORS['gold'],
        padding=(1, 2)
    )
    
    # Brief Meaning Section
    meaning_panel = Panel(
        Text(name.brief_meaning, style=f"{COLORS['meaning']} italic", justify="center"),
        title="[bold]Brief Meaning[/]",
        title_align="center",
        border_style=COLORS['purple'],
        box=ROUNDED,
        padding=(1, 3)
    )
    
    # Ta'wil Section (Four Levels of Meaning)
    if name.tawil:
        tawil_lines = name.tawil.split('\n')
        tawil_text = Text()
        
        for line in tawil_lines:
            if '📿 SHARĪ\'A' in line:
                tawil_text.append(line + "\n", style=f"bold {COLORS['green']}")
            elif '🚶 ṬARĪQA' in line:
                tawil_text.append(line + "\n", style=f"bold {COLORS['purple']}")
            elif '💎 ḤAQĪQA' in line:
                tawil_text.append(line + "\n", style=f"bold {COLORS['gold']}")
            elif '🌟 MA\'RIFA' in line:
                tawil_text.append(line + "\n", style=f"bold {COLORS['light_purple']}")
            else:
                tawil_text.append(line + "\n", style=COLORS['white'])
        
        tawil_panel = Panel(
            tawil_text,
            title="[bold gold]◈ Ta'wīl - The Four Levels of Interpretation ◈[/]",
            title_align="center",
            border_style=COLORS['gold'],
            box=ROUNDED,
            padding=(1, 2),
            expand=True
        )
    else:
        tawil_panel = None
    
    # Quranic References
    if name.quranic_reference or name.verse_ayah:
        ref_table = Table(show_header=False, box=None, padding=(0, 1))
        ref_table.add_column("", style=COLORS['green'])
        
        if name.quranic_reference:
            ref_table.add_row(f"📖 {name.quranic_reference}")
        if name.verse_ayah:
            ref_table.add_row(f"📍 {name.verse_ayah}")
        
        ref_panel = Panel(
            Align.center(ref_table),
            title="[bold]Quranic References[/]",
            title_align="center",
            border_style=COLORS['green'],
            box=ROUNDED
        )
    else:
        ref_panel = None
    
    # Dhikr Formula
    if name.dhikr_formula:
        dhikr_lines = name.dhikr_formula.split('\n')
        dhikr_text = Text()
        
        for line in dhikr_lines:
            if any(arabic in line for arabic in ['يا', 'ی']):  # Contains Arabic
                dhikr_text.append(line + "\n", style=f"bold {COLORS['arabic']}")
            else:
                dhikr_text.append(line + "\n", style=COLORS['white'])
        
        dhikr_panel = Panel(
            Align.center(dhikr_text),
            title="[bold purple]✦ Dhikr Formula ✦[/]",
            title_align="center",
            border_style=COLORS['purple'],
            box=ROUNDED,
            padding=(1, 2)
        )
    else:
        dhikr_panel = None
    
    # Pronunciation Guide
    if name.pronunciation or name.phonetics:
        pron_text = Text()
        if name.pronunciation:
            pron_text.append(f"Pronunciation: {name.pronunciation}\n", style=f"italic {COLORS['light_purple']}")
        if name.phonetics:
            pron_text.append(f"Guide: {name.phonetics}", style=COLORS['white'])
        
        pron_panel = Panel(
            Align.center(pron_text),
            border_style=COLORS['purple'],
            box=ASCII,
            padding=(0, 2)
        )
    else:
        pron_panel = None
    
    # Display all panels
    console.print(title_panel)
    console.print()
    
    if meaning_panel:
        console.print(meaning_panel)
        console.print()
    
    if tawil_panel:
        console.print(tawil_panel)
        console.print()
    
    if ref_panel:
        console.print(ref_panel)
        console.print()
    
    if dhikr_panel:
        console.print(dhikr_panel)
        console.print()
    
    if pron_panel:
        console.print(pron_panel)
    
    # Final blessing
    console.print()
    blessing = Panel(
        Align.center(Text(
            "May this Divine Name illuminate your path today",
            style=f"italic {COLORS['gold']}"
        )),
        box=ROUNDED,
        border_style=COLORS['gold'],
        padding=(1, 2)
    )
    console.print(blessing)


def show_error(message: str) -> None:
    """Display error message"""
    error_panel = Panel(
        Text(message, style="bold red"),
        title="[bold red]Error[/]",
        title_align="center",
        border_style="red",
        box=ROUNDED,
        padding=(1, 2)
    )
    console.print(error_panel)


def show_entropy_report(report: str) -> None:
    """Display entropy report for transparency"""
    console.print()
    report_panel = Panel(
        Text(report, style=f"{COLORS['purple']} dim"),
        title="[bold purple]🔐 Randomness Report[/]",
        title_align="center",
        border_style=COLORS['purple'],
        box=ASCII,
        padding=(1, 2)
    )
    console.print(report_panel)