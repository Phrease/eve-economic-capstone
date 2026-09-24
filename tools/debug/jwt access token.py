import base64
import requests
import urllib.parse
import secrets
import os
from dotenv import load_dontenv

load_dontenv()

# 1. Define your application credentials and settings
CLIENT_ID = os.getenv('SECRET_CLIENT_ID')
CLIENT_SECRET = os.getenv('SECRET_CLIENT_SECRET')
# This must exactly match the callback URL defined in the EVE Developer Portal
CALLBACK_URL = 'http://localhost' 
# The scope required to resolve structure IDs
SCOPES = 'esi-universe.read_structures.v1'

def generate_auth_url():
    """Generates the login URL for the user to authorize the application."""
    state = secrets.token_urlsafe(16)
    base_auth_url = "https://login.eveonline.com/v2/oauth/authorize/"
    
    params = {
        "response_type": "code",
        "redirect_uri": CALLBACK_URL,
        "client_id": CLIENT_ID,
        "scope": SCOPES,
        "state": state
    }
    
    url = f"{base_auth_url}?{urllib.parse.urlencode(params)}"
    return url

def get_access_token(auth_code):
    """Exchanges the authorization code for an access token using Basic Auth."""
    token_url = "https://login.eveonline.com/v2/oauth/token"
    
    # Create the Base64 encoded Basic Auth header
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "login.eveonline.com"
    }
    
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code
    }
    
    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    
    return response.json()

if __name__ == '__main__':
    print("Step 1: Open the following URL in your web browser to log in and authorize the app:")
    print(generate_auth_url())
    print("\nStep 2: After logging in, you will be redirected to a URL that looks broken (localhost).")
    print("Copy the entire URL from your browser's address bar and paste it below.")
    
    redirected_url = input("\nPaste the full redirect URL here: ").strip()
    
    # Extract the 'code' parameter from the pasted URL
    parsed_url = urllib.parse.urlparse(redirected_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    if 'code' in query_params:
        auth_code = query_params['code'][0]
        
        print("\nStep 3: Exchanging authorization code for access token...")
        try:
            token_response = get_access_token(auth_code)
            access_token = token_response.get('access_token')
            
            print("\n--- Success! ---")
            print(f"Access Token: {access_token}\n")
            print("Copy the Access Token above and paste it into your structure discovery script.")
        except requests.exceptions.HTTPError as e:
            print(f"\nHTTP Error during token exchange: {e.response.text}")
    else:
        print("\nError: Could not find the 'code' parameter in the URL. Ensure you copied the entire redirect link.")