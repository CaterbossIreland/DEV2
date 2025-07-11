# graph_auth.py
import os
import requests

def get_access_token() -> str:
    """Get an OAuth2 access token for Microsoft Graph using client credentials."""
    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    if not tenant_id or not client_id or not client_secret:
        raise RuntimeError("Missing TENANT_ID, CLIENT_ID, or CLIENT_SECRET environment variables")

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        try:
            error_json = response.json()
            error_msg = error_json.get("error_description") or error_json.get("error", {}).get("message", "")
        except ValueError:
            error_msg = ""
        raise Exception(f"Failed to obtain access token (HTTP {response.status_code}): {error_msg}")
    
    token = response.json().get("access_token")
    if not token:
        raise Exception("Authentication response did not contain an access token")
    return token
