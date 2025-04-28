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


def modify_template(new_pipeline_path, api_url, schedulingPeriod):

    ## Pipeline intervall
    telegraf_utils.modify_agent(new_pipeline_path,"interval", schedulingPeriod)

    ## API url 
    telegraf_utils.modify_input(new_pipeline_path,"urls", [api_url])






###########################



def build_pipeline():
    if config.INTERACTIVE_MODE:
        data_values, api_url, api_username, api_password= common.get_data_values()

        print("\nKui tihti peaks andmekonveier jooksma? (sekundites)")
        schedulingPeriod = str(common.ask_digit_input(86400))+ "sec"

        new_pipeline_name=input("Mis saab andmekonveieri nimeks: ")+".toml"

    ## TODO
    else:
        api_url = config.API_URL
        data_values = config.API_FIELDS
        schedulingPeriod = config.PIPELINE_SCHEDULING_PERIOD
        new_pipeline_name = config.PIPELINE_NAME+".toml"
        api_username = config.API_USERNAME
        api_password = config.API_PASSWORD




    ### Select template 
    ##TODO
    template_name="basic_ETL.toml"

    new_pipeline_path = f"pipelines/{new_pipeline_name}"
    shutil.copy(f"modules/telegraf/templates/{template_name}", new_pipeline_path)


    modify_template(new_pipeline_path, api_url, schedulingPeriod)
    #telegraf.modify_output("templates/basic_ETL.toml", "urls", "testingIfWorks")






    print("end currently")
    #print(f"✅✅✅ Valmis. Uus genereeritud andmekoveier nimega '{new_pipeline_name}' asub kaustas 'pipelines'.")
