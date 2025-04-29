import config 

import requests
import sys
import json


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
    db_full_url=config.DB_URL+"/write?db="+config.DB_NAME
    update_template(file_path, dot_path, "HTTP URL", db_full_url)

    ## Update username
    update_template(file_path, dot_path, "username", config.DB_USER)

    ## Update username
    update_template(file_path, dot_path, "password", config.DB_PASS)





#   export TOKEN=$(curl -k -X POST https://127.0.0.1.nip.io/nifi-api/access/token\
#                 -H "Content-Type: application/x-www-form-urlencoded" -d 'username=lab08nifiuser&password=tartunifi2023')

def get_access_token():
    token_resp = requests.post(
        f"{config.NIFI_HOST}/nifi-api/access/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": config.NIFI_USER, "password": config.NIFI_PASS},
        verify=False
    )
    token_resp.raise_for_status()
    token = token_resp.text.strip()
    return token


#  curl -sk -X POST "https://127.0.0.1.nip.io/nifi-api/process-groups/root/process-groups/upload" -H "Authorization: Bearer $TOKEN"\
#       -F "file=@pipelines/test_pipeline.json" -F "groupName=MyNewProcessGroup" -F "positionX=0" -F "positionY=0"
#       -F "disconnectedNodeAcknowledged=false" -F "clientId=unique-client-id-123"


def upload_nifi_pipeline(token, pipeline_path, processorGroup_name, username=config.NIFI_USER, password=config.NIFI_PASS, nifi_url=config.NIFI_HOST, position_x=0, position_y=0, client_id = "unique-client-id-123"):

    with open(pipeline_path, "r") as json_file:
        files = {
            "file": json_file,
            "groupName": (None, processorGroup_name),
            "positionX": (None, str(position_x)),
            "positionY": (None, str(position_y)),
            "disconnectedNodeAcknowledged": (None, "false"),
            "clientId": (None, client_id)
        }

        upload_resp = requests.post(
            f"{nifi_url}/nifi-api/process-groups/root/process-groups/upload",
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            verify=False
        )

    upload_resp.raise_for_status()
    print(f"✅ Uploaded process group '{processorGroup_name}' successfully!")
