from pyfiglet import figlet_format
from rich.console import Console


from modules.telegraf import telegraf_utils
#from modules.nifi import nifi_utils
from common import core as common
import config


import toml
import shutil



def introduction():
    console = Console()
    ascii_art = figlet_format("Telegraf")
    console.print(ascii_art, style="cyan")

    print("Valisid Telegraf Platformi!\n")



###########################


def modify_template(new_pipeline_path, api_url, schedulingPeriod, data_values, measurement_name, api_username, api_password, template_name):

    ## Pipeline interval
    telegraf_utils.modify_agent(new_pipeline_path,"interval", schedulingPeriod)

    ## API url 
    telegraf_utils.modify_input(new_pipeline_path,"urls", [api_url])

    ### Pluggins
    fields=[]
    json_query = ""


    if template_name == "basic_ETL.toml":

        for key, value in data_values.items():
            fields.append(key)

            parts = value.rsplit('.', 2)
            json_query = '.'.join(parts[:-1])[1:] # Get the json path till last item (second last dot(.))


        telegraf_utils.modify_input(new_pipeline_path,"json_query", json_query)
        telegraf_utils.modify_input(new_pipeline_path,"fieldinclude", fields)

    elif template_name == "advanced_ETL.toml":

        for key, value in data_values.items():

            parts = value.split(']', 1)
            json_query = parts[0].split("[")[0][1:]
            fields.append(parts[1][1:])



        telegraf_utils.modify_input(new_pipeline_path,"json_query", json_query)
        telegraf_utils.modify_input(new_pipeline_path,"json_string_fields", fields)




    ## Measurement
    telegraf_utils.modify_input(new_pipeline_path,"name_override", measurement_name)

    ## Database
    telegraf_utils.modify_output(new_pipeline_path, "urls", [config.DB_URL])
    telegraf_utils.modify_output(new_pipeline_path, "database", config.DB_NAME)
    telegraf_utils.modify_output(new_pipeline_path, "username", config.DB_USER)
    telegraf_utils.modify_output(new_pipeline_path, "password", config.DB_PASS)


    ## If authenctication needed
    if api_username and api_username.lower() != "placeholder":
        telegraf_utils.modify_input(new_pipeline_path,"username", api_username)
        telegraf_utils.modify_input(new_pipeline_path,"password", api_password)




def build_pipeline():
    if config.INTERACTIVE_MODE:
        data_values, api_url, api_username, api_password= common.get_data_values()

        print("\nKui tihti peaks andmekonveier jooksma? (sekundites)")
        schedulingPeriod = str(common.ask_digit_input(86400))+ "s"
        measurement_name = str(input("Palun sisesta andmebaasi (influxDB) jaoks vajalik 'measurement' nimi: "))
        new_pipeline_name=input("Mis saab andmekonveieri nimeks: ")+".toml"

    ## TODO
    else:
        api_url = config.API_URL
        data_values = config.API_FIELDS
        schedulingPeriod = config.PIPELINE_SCHEDULING_PERIOD+"s"
        new_pipeline_name = config.PIPELINE_NAME+".toml"
        api_username = config.API_USERNAME
        api_password = config.API_PASSWORD
        measurement_name = config.MEASUREMENT_NAME




    ### Select template 
    ##TODO
    #template_name="basic_ETL.toml"
    if (api_username and api_username.lower() != "placeholder") and (api_password and api_password.lower() != "placeholder"):
        template_name="advanced_ETL.toml"
    else:
        template_name="basic_ETL.toml"

    new_pipeline_path = f"pipelines/{new_pipeline_name}"
    shutil.copy(f"modules/telegraf/templates/{template_name}", new_pipeline_path)


    modify_template(new_pipeline_path, api_url, schedulingPeriod, data_values, measurement_name, api_username, api_password, template_name)


    print(f"✅✅✅ Valmis. Uus genereeritud andmekoveier nimega '{new_pipeline_name}' asub kaustas 'pipelines'.")
