import requests
import json
from requests.auth import HTTPBasicAuth


def ask_binary_input(prompt="Kas jah või ei?: ", valikud=["jah","ei"]):
    while True:
        answer = input(prompt).strip().lower()
        if answer in valikud:
            return answer
        print(f"Ebakorretne sisend.Palun vasta kas '{valikud[0]}' või '{valikud[1]}'")

def is_app_url_correct(api_url, needs_auth, username,passwd):
    print("Teostan API kutset...\n")
    try:
        if needs_auth:
            response = requests.get(api_url, auth=HTTPBasicAuth(username, passwd))
        else:
            response = requests.get(api_url)

        response.raise_for_status() ## Check if staus code is 2xx
        data = response.json()
        print(json.dumps(data, indent=2))
        return True

    except requests.exceptions.RequestException as e:
        print(f"HTTP error: {e}")
        return False
    except ValueError:
        print("andmeallikas ei tagasta vallidset JSON kuju...")
        return False
    except Exception as e:
        print(f"API kutsel tekkis viga: {e}")
        return False


##TODO
def add_api_authentication():
    print("Adding api authentication ... (TODO)")

