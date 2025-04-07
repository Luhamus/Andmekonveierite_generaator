from pyfiglet import figlet_format
from rich.console import Console
from common import core as common

import sys
import json
import shutil


def introduction():
    console = Console()
    ascii_art = figlet_format("Nifi")
    console.print(ascii_art, style="cyan")
    print("Valisid Nifi Platformi!\n")


## TODO
def update_template(file_path, dot_path, new_key, new_value):

    # Step 2: Load the copied JSON
    with open(file_path, "r") as f:
        data = json.load(f)

    # Step 3: Walk the path (e.g. 'flowContents.processors[0].properties')
    keys = dot_path.split(".")
    current = data

    for key in keys:
        if key.endswith("]"):  # Handle list index like processors[0]
            list_key = key[:key.index("[")]
            index = int(key[key.index("[") + 1 : key.index("]")])
            current = current[list_key][index]
        else:
            current = current[key]

    # Step 4: Add or update the key
    current[new_key] = new_value
    print(f"🛠 Added '{new_key}': '{new_value}' at path '{dot_path}'")

    # Step 5: Save back the JSON
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
        print("✅ Changes saved.")


### Example Usage ###
# copy_and_modify_json(
#     "template.json",
#     "pipeline_copy.json",
#     "flowContents.processors[1].properties",
#     "New Config Key",
#     "New Config Value"
# )



def get_data_values():

    chosen_json_values = {}

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

                chosen_json_values.update(common.inspect_json_top_level(json_data))
                print("Oled hetkel valinud järgmised väärtused:", ", ".join(chosen_json_values))
                choose_another = common.ask_binary_input(prompt="\nKas soovid (v)alida veel mõne väärtuse või liikuda (e)dasi?(v/e): ",valikud=["v","e"]).strip().lower()

                if choose_another == 'e':
                    return chosen_json_values 
        else:
            choice = common.ask_binary_input(prompt="\nKas soovid URL-i (m)uuta URL-i või (v)äljuda?(m/v): ",valikud=["m","v"]).strip().lower()
            if choice == 'v':
                print("Väljun programmist.")
                sys.exit()


def build_pipeline():
    data_values = get_data_values()

    ## TODO
    shutil.copy("modules/nifi/templates/basic_ETL.json", "pipelines/test_pipeline.json")

    ## TODO

    for key, value in data_values.items() :
        #print (key, value)
        update_template("pipelines/test_pipeline.json", "flowContents.processors[2].properties", key, value)


