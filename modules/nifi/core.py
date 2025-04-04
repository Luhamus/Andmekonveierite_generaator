from pyfiglet import figlet_format
from rich.console import Console

import requests


def introduction():
    console = Console()
    ascii_art = figlet_format("Nifi")
    console.print(ascii_art, style="cyan")

    print("Valisid Nifi Platformi!")



def api_url_validness_check(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        response.json() 
        return True 
    except (requests.exceptions.RequestException, ValueError) as e:
        return False



def build_pipeline():
    api_url = input("Palun sisesta andmete API URL: ").strip()

    if (input("Kas API vajab ka autentimist?(Jah/Ei): ").strip().lower() == 'jah'):
        print("TODO")

    if(api_url_validness_check(api_url)):
        print("Good")
    else:
        print("Bad")
