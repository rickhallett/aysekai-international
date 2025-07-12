"""ASCII art for the Asma al-Husna CLI application"""

MOSQUE_ART = r"""
                              ╔═══════════════════════════════════════╗
                              ║         بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ         ║
                              ╚═══════════════════════════════════════╝
    
                                           .::.
                                         .:::::.
                                       .:::::::::.
                                      ::::::::::::: 
                                     ::::::::::::::: 
                                   ╭─┴─────────────┴─╮
                                  ╱                   ╲
                                 │    ●           ●    │
                                ╱     ╰─────────╯       ╲
                               │                         │
                              ╱━━━━━━━━━━━━━━━━━━━━━━━━━╲
                             │  ┏━━━━━━━━━━━━━━━━━━━━┓  │
                             │  ┃                   ┃  │
                             │  ┃   ●    ●    ●    ┃  │
                             │  ┃                   ┃  │
                            ╱│  ┃  ╭─╮  ╭─╮  ╭─╮  ┃  │╲
                           ╱ │  ┃  │ │  │ │  │ │  ┃  │ ╲
                          ╱  │  ┃  │ │  │ │  │ │  ┃  │  ╲
                         ╱   │  ┗━━┷━┷━━┷━┷━━┷━┷━━┛  │   ╲
                        ╱    └───────────────────────┘    ╲
                       ╱══════════════════════════════════╲
                      ╱════════════════════════════════════╲
                                 اَللّٰهُ أَكْبَر
"""

BAGHDAD_ART = r"""
                     ╔═══════════════════════════════════════════════╗
                     ║              مَدِينَةُ السَّلَامِ                  ║
                     ║            The City of Peace              ║
                     ╚═══════════════════════════════════════════════╝
    
                                    ╭───┬───╮
                                    │░░░│░░░│
                                 ╭──┴───┴───┴──╮
                                 │░░░░░░░░░░░░░│
                              ╭──┴─────────────┴──╮
                              │░░░░░●░░░░░●░░░░░░│
                           ╭──┴───────────────────┴──╮
                           │░░░░░░░░░░░░░░░░░░░░░░░░│
                        ╭──┴─────────────────────────┴──╮
                        │░░░░░╔═══════════════╗░░░░░░░│
                        │░░░░░║               ║░░░░░░░│
                     ╭──┴─────╫    دَارُ الخِلَافَة   ╟─────┴──╮
                     │░░░░░░░░║               ║░░░░░░░░│
                  ╭──┴────────╚═══════════════╝────────┴──╮
                  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
               ╭──┴──────────────────────────────────────┴──╮
               │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
               │▓▓╔══╗▓▓╔══╗▓▓╔══╗▓▓╔══╗▓▓╔══╗▓▓╔══╗▓▓│
               │▓▓║  ║▓▓║  ║▓▓║  ║▓▓║  ║▓▓║  ║▓▓║  ║▓▓│
               ╰──╨──╨──╨──╨──╨──╨──╨──╨──╨──╨──╨──╨──╯
                           دِجْلَة ~ The Tigris River ~
"""

SALUTATION_TEXT = """
                        ╔════════════════════════════════════════╗
                        ║    السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ    ║
                        ║  Peace be upon you and Allah's mercy   ║
                        ║         and His blessings              ║
                        ╚════════════════════════════════════════╝
"""

WELCOME_MESSAGE = """
Welcome to the sacred journey through the 99 Beautiful Names of Allah.

Each name is a gateway to understanding the Divine attributes,
a lamp illuminating the path of spiritual realization.

As the mystics say: "He who knows himself, knows his Lord."
Through contemplation of these names, we polish the mirror of the heart.
"""


def get_intro_art() -> str:
    """Returns the complete introduction art and text"""
    return MOSQUE_ART + "\n" + SALUTATION_TEXT + "\n" + WELCOME_MESSAGE


def get_baghdad_art() -> str:
    """Returns the Baghdad city art"""
    return BAGHDAD_ART + "\n" + SALUTATION_TEXT


def get_divider(style: str = "ornate") -> str:
    """Returns decorative dividers"""
    dividers = {
        "ornate": "════════════════════◈◆◈════════════════════",
        "simple": "─" * 50,
        "double": "═" * 50,
        "stars": "✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦",
        "arabic": "﴿ ﴾ ﴿ ﴾ ﴿ ﴾ ﴿ ﴾ ﴿ ﴾ ﴿ ﴾ ﴿ ﴾",
        "geometric": "◈──────◆──────◈──────◆──────◈",
    }
    return dividers.get(style, dividers["ornate"])


def get_frame_top() -> str:
    """Returns the top of a decorative frame"""
    return "╔═══════════════════════════════════════════════════════════════╗"


def get_frame_bottom() -> str:
    """Returns the bottom of a decorative frame"""
    return "╚═══════════════════════════════════════════════════════════════╝"


def center_text(text: str, width: int = 65) -> str:
    """Centers text within given width"""
    return text.center(width)


def frame_text(text: str, width: int = 63) -> str:
    """Frames text with decorative borders"""
    lines = text.split("\n")
    framed = []

    framed.append(get_frame_top())
    for line in lines:
        if len(line) > width:
            # Wrap long lines
            words = line.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= width:
                    current_line += word + " "
                else:
                    framed.append(f"║ {current_line.strip().ljust(width)} ║")
                    current_line = word + " "
            if current_line:
                framed.append(f"║ {current_line.strip().ljust(width)} ║")
        else:
            framed.append(f"║ {line.ljust(width)} ║")
    framed.append(get_frame_bottom())

    return "\n".join(framed)
