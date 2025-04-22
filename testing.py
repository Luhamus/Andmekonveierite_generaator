import config as config 

import requests
import json

# Configuration
PLAINTEXT_PW = "TODO" 
INPUT_TEMPLATE = "template.json"
OUTPUT_FILE = "configured-flow.json"

# API Endpoints
BASE_URL = f"{config.NIFI_HOST}/nifi-api"
LOGIN_URL = f"{BASE_URL}/access/token"
ENCRYPT_URL = f"{BASE_URL}/flow/encrypt-text"

def get_access_token():
    """Authenticate with NiFi and get JWT token"""
    try:
        response = requests.post(
            LOGIN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"username={config.NIFI_USER}&password={config.NIFI_PASS}",
            verify=False  # For self-signed certificates
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Authentication failed: {str(e)}")
        exit(1)

def encrypt_password(token, plaintext):
    """Encryptpassword using NiFi's API"""
    try:
        response = requests.post(
            ENCRYPT_URL,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {token}"
            },
            data=f"value={plaintext}",
            verify=False
        )
        response.raise_for_status()
        return response.json()["value"]
    except requests.exceptions.RequestException as e:
        print(f"Encryption failed: {str(e)}")
        exit(1)









def update_template(encrypted_pw):
    """Update JSON template with encrypted password"""
    try:
        with open(INPUT_TEMPLATE, "r") as f:
            flow = json.load(f)
        
        # Find and update InvokeHTTP processor
        for processor in flow["flowContents"]["processors"]:
            if processor["type"] == "org.apache.nifi.processors.standard.InvokeHTTP":
                # Update password property
                processor["properties"]["Request password"] = encrypted_pw
                # Mark property as sensitive
                processor["propertyDescriptors"]["Request password"]["sensitive"] = True
                
        with open(OUTPUT_FILE, "w") as f:
            json.dump(flow, f, indent=2)
            
        print(f"Successfully generated: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Template update failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    # 1. Authenticate
    token = get_access_token()

    print("token part DONE")
    
    # 2. Encrypt config.NIFI_PASS
    encrypt_password(token, PLAINTEXT_PW)
    
    # 3. Update template
    #update_template(encrypted_config.NIFI_PASS)
