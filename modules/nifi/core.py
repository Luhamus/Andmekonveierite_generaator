from pyfiglet import figlet_format
from rich.console import Console
from common import core as common

import sys


def introduction():
    console = Console()
    ascii_art = figlet_format("Nifi")
    console.print(ascii_art, style="cyan")
    print("Valisid Nifi Platformi!\n")

def build_pipeline():
    while True:
        api_url = input("Palun sisesta andmete API URL: ").strip()
        username = "placeholder"
        passwd = "placeholder"

        needs_auth = common.ask_binary_input(prompt="Kas API vajab ka kasutajaga autentimist?(jah/ei): ").strip().lower() == 'jah'
        if needs_auth:
            username=input("Sisesta kasutajanimi: ")
            passwd=input("Sisesta parool: ")

        if common.is_app_url_correct(api_url,needs_auth,username,passwd):
            break  # Exit loop if URL is correct
        else:
            choice = common.ask_binary_input(prompt="\nKas soovid URL-i (m)uuta URL-i või (v)äljuda?(m/v): ",valikud=["m","v"]).strip().lower()
            if choice == 'v':
                print("Väljun programmist.")
                sys.exit()
