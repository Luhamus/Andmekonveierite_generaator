import requests
import json

##############################

def extract_snippet_fields(flow):
    return {
        key: flow.get(key, [])
        for key in [
            "processors",
            "connections",
            "funnels",
            "inputPorts",
            "outputPorts",
            "labels",
            "controllerServices",
            "processGroups"
        ]
    }

def upload_nifi_exported_flow(
    nifi_host: str,
    username: str,
    password: str,
    json_file_path: str,
    verify_ssl: bool = False
):
    try:
        token_resp = requests.post(
            f"{nifi_host}/nifi-api/access/token",
            data={"username": username, "password": password},
            verify=verify_ssl
        )
        token_resp.raise_for_status()
        token = token_resp.text

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        root_resp = requests.get(f"{nifi_host}/nifi-api/flow/process-groups/root", headers=headers, verify=verify_ssl)
        root_resp.raise_for_status()
        root_pg_id = root_resp.json()["processGroupFlow"]["id"]

        with open(json_file_path, "r") as f:
            raw = json.load(f)

        flow = raw.get("flowContents")
        if not flow:
            raise ValueError("Missing 'flowContents' in provided file.")

        snippet = extract_snippet_fields(flow)

        payload = {
            "revision": { "version": 0 },
            "component": {
                "name": flow.get("name", "ImportedGroup"),
                "position": { "x": 0.0, "y": 0.0 },
                "flowSnippet": snippet
            }
        }

        url = f"{nifi_host}/nifi-api/process-groups/{root_pg_id}/process-groups"
        resp = requests.post(url, headers=headers, json=payload, verify=verify_ssl)

        if resp.status_code == 201:
            print("✅ Flow uploaded successfully!")
            pg_id = resp.json()["component"]["id"]
            print(f"🔗 View it at: {nifi_host}/nifi/#/process-groups/{root_pg_id}/process-group/{pg_id}")
        else:
            print(f"❌ Upload failed: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"🚨 Error: {e}")







