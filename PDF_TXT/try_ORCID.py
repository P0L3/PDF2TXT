"""ORCID tryout"""

import requests

# Define the URL for token retrieval
url = "https://sandbox.orcid.org/oauth/token"

# Define your client ID and client secret
client_id = "APP-1IXHDD9VQXV3XZ5Q"
client_secret = "06f6d7d5-5b69-4e37-8f2c-3bae4f5070af"

# Define the data payload for the POST request
data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials",
    "scope": "/read-public"
}

# Define headers (if needed)
headers = {
    "Accept": "application/json"
}

# Make the POST request to retrieve the access token
response = requests.post(url, data=data, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the access token from the response JSON
    access_token = response.json().get("access_token")
    print("Access Token:", access_token)
else:
    print("Failed to retrieve the access token. Status code:", response.status_code)