#  import requests
#  import json
#  
#  def extract_snippet_fields(flow):
#      return {
#          key: flow.get(key, [])
#          for key in [
#              "processors",
#              "connections",
#              "funnels",
#              "inputPorts",
#              "outputPorts",
#              "labels",
#              "controllerServices",
#              "processGroups"
#          ]
#      }
#  
#  def upload_nifi_exported_flow(
#      nifi_host: str,
#      username: str,
#      password: str,
#      json_file_path: str,
#      verify_ssl: bool = False
#  ):
#      try:
#          token_resp = requests.post(
#              f"{nifi_host}/nifi-api/access/token",
#              data={"username": username, "password": password},
#              verify=verify_ssl
#          )
#          token_resp.raise_for_status()
#          token = token_resp.text
#  
#          headers = {
#              "Authorization": f"Bearer {token}",
#              "Content-Type": "application/json"
#          }
#  
#          root_resp = requests.get(f"{nifi_host}/nifi-api/flow/process-groups/root", headers=headers, verify=verify_ssl)
#          root_resp.raise_for_status()
#          root_pg_id = root_resp.json()["processGroupFlow"]["id"]
#  
#          with open(json_file_path, "r") as f:
#              raw = json.load(f)
#  
#          flow = raw.get("flowContents")
#          if not flow:
#              raise ValueError("Missing 'flowContents' in provided file.")
#  
#          snippet = extract_snippet_fields(flow)
#  
#          payload = {
#              "revision": { "version": 0 },
#              "component": {
#                  "name": flow.get("name", "ImportedGroup"),
#                  "position": { "x": 0.0, "y": 0.0 },
#                  "flowSnippet": snippet
#              }
#          }
#  
#          url = f"{nifi_host}/nifi-api/process-groups/{root_pg_id}/process-groups"
#          resp = requests.post(url, headers=headers, json=payload, verify=verify_ssl)
#  
#          if resp.status_code == 201:
#              print("✅ Flow uploaded successfully!")
#              pg_id = resp.json()["component"]["id"]
#              print(f"🔗 View it at: {nifi_host}/nifi/#/process-groups/{root_pg_id}/process-group/{pg_id}")
#          else:
#              print(f"❌ Upload failed: {resp.status_code} - {resp.text}")
#  
#      except Exception as e:
#          print(f"🚨 Error: {e}")
#  
#  
#  
#  
#  #####################################################################################
#  
#  
#  def get_nifi_token(nifi_url, username, password, verify_ssl=False):
#      """
#      Get authentication token from NiFi.
#      """
#      token_url = f"{nifi_url}/access/token"
#      headers = {
#          "Content-Type": "application/x-www-form-urlencoded"
#      }
#      data = {
#          "username": username,
#          "password": password
#      }
#  
#      response = requests.post(token_url, headers=headers, data=data, verify=verify_ssl)
#      
#      if response.ok:
#          return response.text
#      else:
#          print(f"Failed to get token: {response.status_code}")
#          print(response.text)
#          response.raise_for_status()
#  
#  def get_root_process_group_id(nifi_url, token, verify_ssl=False):
#      """
#      Get the root process group ID from NiFi.
#      """
#      root_url = f"{nifi_url}/flow/process-groups/root"
#      headers = {
#          "Authorization": f"Bearer {token}"
#      }
#  
#      response = requests.get(root_url, headers=headers, verify=verify_ssl)
#  
#      if response.ok:
#          return response.json()["processGroupFlow"]["id"]
#      else:
#          print(f"Failed to get root process group ID: {response.status_code}")
#          print(response.text)
#          response.raise_for_status()
#  
#  
#  def upload_nifi_pipeline_nifi_2_1(file_path, nifi_url, username, password, process_group_id=None, verify_ssl=False):
#      """
#      Authenticate to NiFi 2.1+, fetch root process group ID, and upload the flow definition JSON.
#      """
#      token = get_nifi_token(nifi_url, username, password, verify_ssl)
#  
#      if not process_group_id:
#          process_group_id = get_root_process_group_id(nifi_url, token, verify_ssl)
#  
#      with open(file_path, 'r') as f:
#          pipeline_json = json.load(f)
#  
#      import_endpoint = f"{nifi_url}/versions/process-groups/{process_group_id}/import"
#      headers = {
#          "Content-Type": "application/json",
#          "Accept": "application/json",
#          "Authorization": f"Bearer {token}"
#      }
#  
#      response = requests.post(
#          import_endpoint,
#          headers=headers,
#          data=json.dumps(pipeline_json),
#          verify=verify_ssl
#      )
#  
#      if response.ok:
#          print("✅ Pipeline uploaded successfully (NiFi 2.1).")
#          return response.json()
#      else:
#          print(f"❌ Failed to upload pipeline: {response.status_code}")
#          print(response.text)
#          response.raise_for_status()
#  
#  
#  
#  #################### Testing ###################
#  upload_nifi_pipeline_nifi_2_1(
#      file_path="templates/basic_ETL.json",
#      nifi_url="https://127.0.0.1.nip.io/nifi-api",
#      username="lab08nifiuser",
#      password="tartunifi2023",
#      #process_group_id="5bb69687-0194-1000-ce98-931e7e192b3d",
#      verify_ssl=False  # set to True if using trusted SSL certs
#  )
