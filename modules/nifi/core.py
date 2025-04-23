## TODO - check syntax
from common import core as common
import config as config 
from modules.nifi import nifi_utils


from pyfiglet import figlet_format
from rich.console import Console
import sys
import json
import shutil
import requests
import re
import base64


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
                ## Testing
                print("Oled hetkel valinud järgmised väärtused JSON lõppväärtused: ", ", ".join(chosen_json_values))
                choose_another = common.ask_binary_input(prompt="\nKas soovid (v)alida veel mõne väärtuse või liikuda (e)dasi?(v/e): ",valikud=["v","e"]).strip().lower()

                if choose_another == 'e':
                    return chosen_json_values, api_url, username, passwd
        else:
            choice = common.ask_binary_input(prompt="\nKas soovid URL-i (m)uuta URL-i või (v)äljuda?(m/v): ",valikud=["m","v"]).strip().lower()
            if choice == 'v':
                print("Väljun programmist.")
                sys.exit()

                


## TODO - textReplace part -> fix templates
def modify_all_processors(data_values, schedulingPeriod, new_pipeline_name, api_url, api_username, api_password):
    ############### Choosing and modfyfing Template ##############

    ### Check if splitJson template needed
    needs_SplitJson = False
    path_parts = []
    for el in data_values.values():
        if '[' in el:
            needs_SplitJson = True
            #path_parts = el.split(']')
            path_parts = re.split(r'(?<=\])', el)



    ### Select template 
    ## TODO - currently has only 2 templates...
    if needs_SplitJson:
        template_name="splitJsonETL.json"
    else:
        template_name="basic_ETL.json"

    new_pipeline_path = f"pipelines/{new_pipeline_name}"
    shutil.copy(f"modules/nifi/templates/{template_name}", new_pipeline_path)



    ### Processor editing

    ## Measurements name defining
    if config.INTERACTIVE_MODE:
        measurements_name = str(input("Palun sisesta andmebaasi jaoks vajalik 'measurement' nimi (influxDB): "))
    else:
        measurements_name = config.NIFI_MEASUREMENT_NAME+" "


    if needs_SplitJson:
        ## SplitJson update
        split_json_path = "$"+re.sub(r'\[(.*?)\]', r'[*]', path_parts[0])
        update_template(new_pipeline_path, "flowContents.processors[3].properties", "JsonPath Expression", split_json_path)

        ## EvaluateJsonPath processor setup
        for key, value in data_values.items() :
            path_parts = value.split(']')
            update_template(new_pipeline_path, "flowContents.processors[2].properties", key, "$"+path_parts[1])
            measurements_name+=f"{key}=${{{key}}},"

        ## Database Setup
        set_database_credentials(new_pipeline_path, "flowContents.processors[4].properties")
    else:
        ## EvaluateJsonPath processor setup
        for key, value in data_values.items() :
            update_template(new_pipeline_path, "flowContents.processors[2].properties", key, "$"+value)
            measurements_name+=f"{key}=${{{key}}},"

        ## Database Setup
        set_database_credentials(new_pipeline_path, "flowContents.processors[3].properties")

    ## ReplaceText processor update - making it compatible for timeseries database (influxDB)
    update_template(new_pipeline_path, "flowContents.processors[0].properties", "Replacement Value", measurements_name[:-1]) # Delete last coma

    ## Update API call URL
    update_template(new_pipeline_path, "flowContents.processors[1].properties", "HTTP URL", api_url)

    ## Update scheduling Periond on API Calls
    update_template(new_pipeline_path, "flowContents.processors[1]", "schedulingPeriod", schedulingPeriod)

    ## Add api credentials
    if api_username != "placeholder":
        update_template(new_pipeline_path, "flowContents.processors[1].properties", "Request Username", api_username)
        update_template(new_pipeline_path, "flowContents.processors[1].properties", "Request Password", api_password)




###############################################

def build_pipeline():

    if config.INTERACTIVE_MODE:
        data_values, api_url, api_username, api_password= get_data_values()

        print("\nKui tihti peaks andmekonveier jooksma? (sekundites)")
        schedulingPeriod = str(common.ask_digit_input(86400))+ "sec"

        new_pipeline_name=input("Mis saab andmekonveieri nimeks: ")+".json"

    else:
        api_url = config.API_URL
        data_values = config.API_FIELDS
        schedulingPeriod = config.PIPELINE_SCHEDULING_PERIOD
        new_pipeline_name = config.PIPELINE_NAME
        api_username = config.API_USERNAME
        api_password = config.API_PASSWORD

    modify_all_processors(data_values, schedulingPeriod, new_pipeline_name, api_url, api_username, api_password)
    print(f"✅✅✅ Valmis. Uus genereeritud andmekoveier nimega '{new_pipeline_name}' asub kaustas 'pipelines'.")



    ## Pipeline Deployment
    if (config.NIFI_DEPLOY):
        token = nifi_utils.get_access_token()
        nifi_utils.upload_nifi_pipeline(token, "pipelines/test_pipeline.json", "test_pipeline", username=config.NIFI_USER, password=config.NIFI_PASS, nifi_url=config.NIFI_HOST, position_x=0, position_y=0)
    else:
        choice = common.ask_binary_input(prompt="\nKas soovid genereeritud andmekonveieri nifi platvormile paigaldada?(jah/ei): ",valikud=["jah","ei"]).strip().lower()
        if choice == "jah":
            token = nifi_utils.get_access_token()
            nifi_utils.upload_nifi_pipeline(token, "pipelines/test_pipeline.json", "test_pipeline", username=config.NIFI_USER, password=config.NIFI_PASS, nifi_url=config.NIFI_HOST, position_x=0, position_y=0)

