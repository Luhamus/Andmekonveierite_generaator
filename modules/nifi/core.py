## TODO - check syntax
from common import core as common
import config as config 
from modules.nifi import nifi_utils as nifi_utils


from pyfiglet import figlet_format
from rich.console import Console
import sys
import json
import shutil
import requests
import re


def introduction():
    console = Console()
    ascii_art = figlet_format("Nifi")
    console.print(ascii_art, style="cyan")
    print("Valisid Nifi Platformi!\n")


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




def set_database_credentials(file_path,dot_path):
    ## Update URL
    update_template(file_path, dot_path, "HTTP URL", config.DB_URL)

    ## Update username
    update_template(file_path, dot_path, "username", config.DB_USER)

    ## Update username
    update_template(file_path, dot_path, "password", config.DB_PASS)





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

                chosen_json_values.update(common.inspect_json_top_level_test(json_data))
                print("Oled hetkel valinud järgmised väärtused JSON lõppväärtused: ", ", ".join(chosen_json_values))
                choose_another = common.ask_binary_input(prompt="\nKas soovid (v)alida veel mõne väärtuse või liikuda (e)dasi?(v/e): ",valikud=["v","e"]).strip().lower()

                if choose_another == 'e':
                    return chosen_json_values 
        else:
            choice = common.ask_binary_input(prompt="\nKas soovid URL-i (m)uuta URL-i või (v)äljuda?(m/v): ",valikud=["m","v"]).strip().lower()
            if choice == 'v':
                print("Väljun programmist.")
                sys.exit()

                


## TODO - textReplace part -> fix templates

def build_pipeline():
    data_values = get_data_values()
    
    ### Check if splitJson template needed
    needs_SplitJson = False
    path_parts = []
    for el in data_values.values():
        if '[' in el:
            needs_SplitJson = True
            #path_parts = el.split(']')
            path_parts = re.split(r'(?<=\])', el)



    ### Select template 
    ## TODO - unhardcoded template usage
    new_pipeline_name="test_pipeline.json"
    if needs_SplitJson:
        template_name="splitJsonETL.json"
    else:
        template_name="basic_ETL.json"

    new_pipeline_path = f"pipelines/{new_pipeline_name}"
    shutil.copy(f"modules/nifi/templates/{template_name}", new_pipeline_path)



    ### Processor editing
    ## Measurements setup - TODO: hardcoded.
    measurements_name = "test_measurementName, "

    if needs_SplitJson:
        ## SplitJson update
        split_json_path = "$"+re.sub(r'\[(.*?)\]', r'[*]', path_parts[0])
        update_template(new_pipeline_path, "flowContents.processors[3].properties", "JsonPath Expression", split_json_path)

        ## EvaluateJsonPath processor setup
        for key, value in data_values.items() :
            path_parts = value.split(']')
            update_template(new_pipeline_path, "flowContents.processors[2].properties", key, "$"+path_parts[1])
            measurements_name+=f"{key}={{{key}}}"

        ## Database Setup
        set_database_credentials(new_pipeline_path, "flowContents.processors[4].properties")
    else:
        ## EvaluateJsonPath processor setup
        for key, value in data_values.items() :
            update_template(new_pipeline_path, "flowContents.processors[2].properties", key, "$"+value)
            measurements_name+=f"{key}={{{key}}}"

        ## Database Setup
        set_database_credentials(new_pipeline_path, "flowContents.processors[3].properties")


    ##ReplaceText update
    update_template(new_pipeline_path, "flowContents.processors[0].properties", "Replacement Value", measurements_name)



    print(f"✅✅✅ Valmis. Uus genereeritud andmekoveier asub siin: {new_pipeline_path}.")



    ## Pipeline Deployment
    if (config.NIFI_DEPLOY):
        nifi_utils.upload_nifi_exported_flow( nifi_host=config.NIFI_HOST, username=config.NIFI_USER, password=config.NIFI_PASS, json_file_path="pipelines/test_pipeline.json", verify_ssl=False)
        print("Andmekonveier on deploytud - TODO")
