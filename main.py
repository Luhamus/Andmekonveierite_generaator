from modules.nifi import core as nifi
from modules.telegraf import core as telegraf

AVAILABLE_PLATFORMS = {
    "1": ("Nifi", nifi),
    "2": ("Telegraf", telegraf)}


def list_platforms():
    print("Available platforms:")
    for key, (name, _) in AVAILABLE_PLATFORMS.items():
        print(f"{key}. {name}")


def main():
    list_platforms()
    plat_choice = input("Palun vali platform (number): ").strip()

    platform = AVAILABLE_PLATFORMS.get(plat_choice)
    if not platform:
        print("Ebaõnnestunud valik, sulgen rakenduse...")
        return

    name, module = platform
    module.introduction()
    module.build_pipeline()


if __name__ == "__main__":
    main()
