from common import core as common
import config
from modules.nifi import nifi_utils

from pyfiglet import figlet_format
from rich.console import Console

import shutil
import re


def introduction():
    console = Console()
    ascii_art = figlet_format("Nifi")
    console.print(ascii_art, style="cyan")
    print("Valisid Nifi Platformi!\n")



def modify_all_processors(data_values, schedulingPeriod, new_pipeline_name, api_url, api_username, api_password):
    """
    data_values: valitud andmeväljad, mida konveier filtreerib
    scedulingPeriod: kui tihti konveier jookseb
    new_pipeline_name: uue konveieri nimi
    api_url: andmete tõmbamise API url
    api_username: Olemasolu korral API kasutaja nimi
    api_parool: Olemasolu korral API kasutaja parool

    Teeb mallis kõik vajalikud muudatused andmekonveieri valmimiseks
    """


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
    if needs_SplitJson:
        template_name="splitJsonETL.json"
    else:
        template_name="basic_ETL.json"

    new_pipeline_path = f"pipelines/{new_pipeline_name}"
    shutil.copy(f"modules/nifi/templates/{template_name}", new_pipeline_path)


    ### Processor editing

    ## Measurements name defining
    if config.INTERACTIVE_MODE:
        measurements_name = str(input("Palun sisesta andmebaasi jaoks vajalik 'measurement' nimi (influxDB): "))+" "
    else:
        measurements_name = config.MEASUREMENT_NAME+" "


    if needs_SplitJson:
        ## SplitJson update
        split_json_path = "$"+re.sub(r'\[(.*?)\]', r'[*]', path_parts[0])
        nifi_utils.update_template(new_pipeline_path, "flowContents.processors[3].properties", "JsonPath Expression", split_json_path)

        ## EvaluateJsonPath processor setup
        for key, value in data_values.items() :
            path_parts = value.split(']')
            nifi_utils.update_template(new_pipeline_path, "flowContents.processors[2].properties", key, "$"+path_parts[1])
            measurements_name+=f"{key}=${{{key}}},"

        ## Database Setup
        nifi_utils.set_database_credentials(new_pipeline_path, "flowContents.processors[4].properties")
    else:
        ## EvaluateJsonPath processor setup
        for key, value in data_values.items() :
            nifi_utils.update_template(new_pipeline_path, "flowContents.processors[2].properties", key, "$"+value)
            measurements_name+=f"{key}=${{{key}}},"

        ## Database Setup
        nifi_utils.set_database_credentials(new_pipeline_path, "flowContents.processors[3].properties")

    ## ReplaceText processor update - making it compatible for timeseries database (influxDB)
    nifi_utils.update_template(new_pipeline_path, "flowContents.processors[0].properties", "Replacement Value", measurements_name[:-1]) # Delete last coma

    ## Update API call URL
    nifi_utils.update_template(new_pipeline_path, "flowContents.processors[1].properties", "HTTP URL", api_url)

    ## Update scheduling Periond on API Calls
    nifi_utils.update_template(new_pipeline_path, "flowContents.processors[1]", "schedulingPeriod", schedulingPeriod)

    ## Add api credentials
    if api_username != "placeholder":
        nifi_utils.update_template(new_pipeline_path, "flowContents.processors[1].properties", "Request Username", api_username)
        nifi_utils.update_template(new_pipeline_path, "flowContents.processors[1].properties", "Request Password", api_password)


###


def build_pipeline():
    """
    Ehitab andmekonveieri kokku ning paigaldab soovi korral ka platvormile
    """

    if config.INTERACTIVE_MODE:
        data_values, api_url, api_username, api_password= common.get_data_values()
        print(data_values)

        print("\nKui tihti peaks andmekonveier jooksma? (sekundites)")
        schedulingPeriod = str(common.ask_digit_input(86400))+ "sec"

        new_pipeline_name=input("Mis saab andmekonveieri nimeks: ")+".json"

    else:
        api_url = config.API_URL
        data_values = config.API_FIELDS
        schedulingPeriod = config.PIPELINE_SCHEDULING_PERIOD+"sec"
        new_pipeline_name = config.PIPELINE_NAME+".json"
        api_username = config.API_USERNAME
        api_password = config.API_PASSWORD

    modify_all_processors(data_values, schedulingPeriod, new_pipeline_name, api_url, api_username, api_password)
    print(f"✅✅✅ Valmis. Uus genereeritud andmekoveier nimega '{new_pipeline_name}' asub kaustas 'pipelines'.")


    ## Pipeline Deployment
    if (config.NIFI_DEPLOY):
        token = nifi_utils.get_access_token()
        nifi_utils.upload_nifi_pipeline(token, f"pipelines/{new_pipeline_name}", new_pipeline_name.split(".")[0], username=config.NIFI_USER, password=config.NIFI_PASS, nifi_url=config.NIFI_HOST, position_x=0, position_y=0)
    else:
        choice = common.ask_binary_input(prompt="\nKas soovid genereeritud andmekonveieri nifi platvormile paigaldada?(jah/ei): ",valikud=["jah","ei"]).strip().lower()
        if choice == "jah":
            token = nifi_utils.get_access_token()
            nifi_utils.upload_nifi_pipeline(token, f"pipelines/{new_pipeline_name}", new_pipeline_name.split(".")[0], username=config.NIFI_USER, password=config.NIFI_PASS, nifi_url=config.NIFI_HOST, position_x=0, position_y=0)
