import requests
import json
from requests.auth import HTTPBasicAuth


def ask_binary_input(prompt="Kas jah või ei?: ", valikud=["jah","ei"]):
    while True:
        answer = input(prompt).strip().lower()
        if answer in valikud:
            return answer
        print(f"Ebakorretne sisend.Palun vasta kas '{valikud[0]}' või '{valikud[1]}'")


def ask_digit_input(max_index):
    while True:
        user_input = input(f"Vali number (0 - {max_index}): ").strip()

        if not user_input.isdigit():
            print("Palun vali korrektne numer.")
            continue # algusesse

        index = int(user_input)

        if 0 <= index <= max_index:
            return int(index)
        else:
            print(f" Number ei kuulu valikusse. Palun vali number vahemikus 0-{max_index}.")



def is_app_url_correct(api_url, needs_auth, username,passwd):
    print("Teostan API kutset...\n")
    try:
        if needs_auth:
            response = requests.get(api_url, auth=HTTPBasicAuth(username, passwd))
        else:
            response = requests.get(api_url)

        response.raise_for_status() ## Check if staus code is 2xx
        data = response.json()
#        print(json.dumps(data, indent=2))
        return data, True

    except requests.exceptions.RequestException as e:
        print(f"HTTP error: {e}")
        return None, False
    except ValueError:
        print("andmeallikas ei tagasta vallidset JSON kuju...")
        return None, False
    except Exception as e:
        print(f"API kutsel tekkis viga: {e}")
        return None, False


## Func todo - add list level support with porcessors etc
def inspect_json_top_level(json_data):
    while True:
        print(json.dumps(json_data, indent=2))
        print("\nVali json võti millest soovid väärtuse andmekonveieriga ekstrakteerida\n")

        keys = list(json_data.keys())

        for index, key in enumerate(keys):
            value = json_data[key]
            value_type = type(value).__name__ ## Mis type json itemgiga tegu
            if isinstance(value, list):
                suggestion = "SplitJson"
            else:
                suggestion = "EvaluateJsonPath"
            print(f"  [{index}] {key} ({value_type})")

        selected_index = ask_digit_input(len(list(json_data.keys())) - 1)
        selected_key = keys[selected_index]
        selected_value = json_data[selected_key]

        # Wrap into new json object
        #extracted = {selected_key: selected_value}

        if isinstance(selected_value, dict) or isinstance(selected_value,list):
            json_data = selected_value
            continue
        else:
            print(f"\nValitud võti: '{selected_key}':")
            #print(json.dumps(selected_value, indent=2))
            return selected_key
