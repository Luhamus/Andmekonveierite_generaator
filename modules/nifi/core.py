from pyfiglet import figlet_format
from rich.console import Console
from common import core as common

import sys
import json


def introduction():
    console = Console()
    ascii_art = figlet_format("Nifi")
    console.print(ascii_art, style="cyan")
    print("Valisid Nifi Platformi!\n")


## TODO
def set_processor_property(pipeline, processor_name, property_key, property_value):
    for processor in pipeline['flowContents']['processors']:
        if processor['name'] == processor_name:
            processor['properties'][property_key] = property_value
            print(f"Updated '{property_key}' in processor '{processor_name}'")
            return
    print(f"Processor '{processor_name}' not found.")







def build_pipeline():

    chosen_json_values = []

    ##Getting API url and json values
    while True:
        api_url = input("Palun sisesta andmete API URL: ").strip()
        username = "placeholder"
        passwd = "placeholder"

        needs_auth = common.ask_binary_input(prompt="Kas API vajab ka kasutajaga autentimist?(jah/ei): ").strip().lower() == 'jah'
        if needs_auth:
            username=input("Sisesta kasutajanimi: ")
            passwd=input("Sisesta parool: ")

        json_data, api_url_correct = common.is_app_url_correct(api_url,needs_auth,username,passwd)

        ## TODO itemite eemaldamise v6malus
        if api_url_correct:
            while True:
                chosen_json_values.append(common.inspect_json_top_level(json_data))
                print("Oled hetkel valinud järgmised väärtused:", chosen_json_values)
                choose_another = common.ask_binary_input(prompt="\nKas soovid (v)alida veel mõne väärtuse või liikuda (e)dasi?(v/e): ",valikud=["v","e"]).strip().lower()

                if choose_another == 'e':
                    return chosen_json_values 

        else:
            choice = common.ask_binary_input(prompt="\nKas soovid URL-i (m)uuta URL-i või (v)äljuda?(m/v): ",valikud=["m","v"]).strip().lower()
            if choice == 'v':
                print("Väljun programmist.")
                sys.exit()
