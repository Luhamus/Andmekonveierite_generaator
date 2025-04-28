from modules.nifi import core as nifi
from modules.telegraf import core as telegraf
import config
import sys

AVAILABLE_PLATFORMS = {
    "1": ("Nifi", nifi),
    "2": ("Telegraf", telegraf)}


def list_platforms():
    print("Platovormide valik:")
    for key, (name, _) in AVAILABLE_PLATFORMS.items():
        print(f"{key}. {name}")


def main():

    ## Kontrolli kas platform andi käsureamuutujana
    if len(sys.argv) >= 2:
        platform = sys.argv[1].lower()
        if platform not in ("telegraf", "nifi"):
            print("Kasutus: main.py [nifi|telegraf]")
            sys.exit(1)
        if platform == "nifi":
            platform = AVAILABLE_PLATFORMS.get("1")
        elif platform == "telegraf": 
            platform = AVAILABLE_PLATFORMS.get("2")

    else:
        ## Vali platvorm
        try:
            if config.PLATFORM.lower() == "nifi":
                platform = AVAILABLE_PLATFORMS.get("1")
            elif config.PLATFORM.lower() == "telegraf": 
                platform = AVAILABLE_PLATFORMS.get("2")
            else:
                raise Exception("Ebaõnnestunud platvormivalik konfiguratsioonifailis...")
        except Exception as e:
            ## ära prindi errorit kui platvormi pole defineeritud
            if isinstance(e, AttributeError):
                pass
            else:
                print(f"Error occurred: {e}")

            list_platforms()
            plat_choice = input("Palun vali platform (number): ").strip()

            platform = AVAILABLE_PLATFORMS.get(plat_choice)
            if not platform:
                print("Ebaõnnestunud valik, sulgen rakenduse...")
                return


    ## Genereeri andmekonveier
    name, module = platform
    module.introduction()
    module.build_pipeline()


if __name__ == "__main__":
    main()
