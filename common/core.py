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


## Checks if api url is correct, if so then returns the json
def is_app_url_correct(api_url, needs_auth, username,passwd):
    print("Teostan API kutset...\n")
    try:
        if needs_auth:
            response = requests.get(api_url, auth=HTTPBasicAuth(username, passwd))
        else:
            response = requests.get(api_url)

        response.raise_for_status() ## Check if staus code is 2xx
        data = response.json()
        #print(json.dumps(data, indent=2))
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


## TODO - add list level support with porcessors etc
## Asks the user json item to extract and returns it as dict item-value pair, where item is name and value json path
def inspect_json_top_level(json_data):
    path = ""

    while True:
        print(json.dumps(json_data, indent=2))
        print("\nVali json võti millest soovid väärtuse andmekonveieriga ekstrakteerida\n")

        keys = list(json_data.keys())

        for index, key in enumerate(keys):
            value = json_data[key]
            value_type = type(value).__name__ ## näitab mis json itemi type'i 
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
            path += "." + selected_key
            continue
        else:
            print(f"\nValitud võti: '{selected_key}':")
            path += "." + selected_key
            return {selected_key: path}





###### Other option ##########

def inspect_json_top_level_test(json_data, has_list=False):
    path = ""
    last_key = "value" #Placeholder

    while True:
        print(json.dumps(json_data, indent=2))
        print("\nVali json võti või indeks millest soovid väärtuse andmekonveieriga ekstrakteerida\n")

        if isinstance(json_data, dict):
            keys = list(json_data.keys())
            for index, key in enumerate(keys):
                value = json_data[key]
                value_type = type(value).__name__
                suggestion = "SplitJson" if isinstance(value, list) else "EvaluateJsonPath"
                print(f"  [{index}] {key} ({value_type}) → {suggestion}")

            selected_index = ask_digit_input(len(keys) - 1)
            selected_key = keys[selected_index]
            selected_value = json_data[selected_key]
            path += "." + selected_key
            last_key = selected_key

        elif isinstance(json_data, list):
            has_list = True
            for index, item in enumerate(json_data):
                item_type = type(item).__name__
                print(f"  [{index}] [{item_type}]")

            selected_index = ask_digit_input(len(json_data) - 1)
            selected_value = json_data[selected_index]
            path += f"[{selected_index}]"
            last_key = str(selected_index)

        else:
            # Primitive value, nothing to dive into
            print(f"\nLõppväärtus: {json_data}")
            return {last_key: path}



        if isinstance(selected_value, (dict, list)):
            json_data = selected_value
        else:
            #print(f"\nValitud väärtus: '{selected_value}'")
            print(f"\nValitud väärtus: '{path}'")
            return {last_key: path}

