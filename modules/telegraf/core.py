from pyfiglet import figlet_format
from rich.console import Console


def introduction():
    console = Console()
    ascii_art = figlet_format("Telegraf")
    console.print(ascii_art, style="cyan")

    print("Valisid Telegraf Platformi!\n")
